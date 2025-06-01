from datetime import timedelta

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openpyxl.cell import MergedCell
from openpyxl.chart import Reference, PieChart
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from io import BytesIO
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from api.models import Operation, Category, Target
from api.serializers import OperationSerializer

class OperationPDFView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OperationSerializer

    def get_queryset(self):
        days = int(self.request.query_params.get('days', 30))
        date_from = timezone.now() - timedelta(days=days)

        queryset = Operation.objects.filter(
            user=self.request.user,
            created_at__gte=date_from
        )

        operation_type = self.request.query_params.get('type')
        if operation_type:
            queryset = queryset.filter(type=operation_type)

        return queryset.select_related('categories').order_by('-created_at')

    @swagger_auto_schema(
        operation_id='Получение выписки в формате pdf',
        operation_description='Получение PDF файла с операциями и диаграммой',
        manual_parameters=[
            openapi.Parameter(
                name="type",
                in_=openapi.IN_QUERY,
                description="Фильтр по типу операций",
                type=openapi.TYPE_STRING,
                enum=["targets", "outcome", "income"],
                required=True,
            ),
            openapi.Parameter(
                name="days",
                in_=openapi.IN_QUERY,
                description="Количество дней для фильтрации",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="PDF файл успешно получен"),
            500: openapi.Response(description="Ошибка генерации отчёта")
        }
    )
    def get(self, request):
        pdfmetrics.registerFont(TTFont('Bold', 'font/bold.ttf'))
        pdfmetrics.registerFont(TTFont('Regular', 'font/Regular.ttf'))
        operations = []
        total = 0.0
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        query = self.request.query_params.get('type')
        for operation in serializer.data:
            amount_str = str(operation['amount'])
            amount = float(amount_str.replace(' ', '').replace(',', '.'))
            total += amount

            formatted_amount = "{:,.2f}".format(amount).replace(",", " ")
            if query == "income" or query == "outcome":
                operations.append({
                    "category": Category.objects.get(id=operation["categories"]).name,
                    "amount": formatted_amount,
                    "date": operation["date"],
                    "_raw_amount": amount
                })
            elif query == "targets":
                operations.append({
                    "target": Target.objects.get(id=operation["target"]).name,
                    "amount": formatted_amount,
                    "date": operation["date"],
                    "_raw_amount": amount
                })
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                    leftMargin=2 * cm, rightMargin=2 * cm,
                                    topMargin=2 * cm, bottomMargin=2 * cm,
                                    encoding='utf-8')

            elements = []
            styles = getSampleStyleSheet()
            font_name = 'Regular'
            bold = "Bold"
            styles['Title'].fontName = font_name
            styles['Normal'].fontName = font_name

            title = Paragraph("Freenance", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 0.5 * cm))
            if query == "income" or query == "outcome":
                table_data = [
                    ["Date", "Category", "Amount"]
                ]
                for op in operations:
                    table_data.append([
                        op['date'],
                        op['target'],
                        op['amount']
                    ])
            elif query == "targets":
                table_data = [
                    ["Date", "Target", "Amount"]
                ]
                for op in operations:
                    table_data.append([
                        op['date'],
                        op['target'],
                        op['amount']
                    ])


            formatted_total = "{:,.2f}".format(total).replace(",", " ")
            table_data.append([
                "",
                "Total",
                formatted_total
            ])
            table = Table(table_data, colWidths=[6 * cm, 6 * cm, 6 * cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3A5FCD')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F0F8FF')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),

                ('FONTNAME', (1, -1), (3, -1), bold),
            ]))

            elements.append(table)

            doc.build(elements)
            buffer.seek(0)

            pdf_data = buffer.getvalue()
            if len(pdf_data) < 100:
                raise ValueError("Generated PDF is empty")

            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="freenance_report.pdf"'
            return response

        except Exception as e:
            return HttpResponse(
                f"Error generating PDF: {str(e)}",
                status=500,
                content_type='text/plain'
            )


class OperationXLSView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OperationSerializer

    def get_queryset(self):
        days = self.request.query_params.get('days')
        now = timezone.now()
        date = now - timedelta(days=int(days))

        queryset = Operation.objects.filter(
            user=self.request.user,
            created_at__gte=date
        )

        operation_type = self.request.query_params.get('type')

        if operation_type:
            queryset = queryset.filter(type=operation_type)

        return queryset.order_by('-created_at')


    @swagger_auto_schema(
        operation_id='Получение выписки в формате xls',
        operation_description='Получение .xls файла',
        manual_parameters=[
            openapi.Parameter(
                name="type",
                in_=openapi.IN_QUERY,
                description="Фильтр по типу операций",
                type=openapi.TYPE_STRING,
                enum=["targets", "outcome", "income"],
                required=True,
            ),
            openapi.Parameter(
                name="days",
                in_=openapi.IN_QUERY,
                description="Количество дней для фильтрации",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses = {
            200: openapi.Response(description="Файл успешно получен", schema=OperationSerializer),
    })
    def get(self, request):
        operations = []
        total = 0.00
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        query = self.request.query_params.get('type')
        # try:
        buffer = BytesIO()
        wb = Workbook()
        ws = wb.active
        ws.title = "Freenance"
        headers = ["Date", "Category", "Amount"]
        data = {}
        for operation in serializer.data:
            if query == "income" or query == "outcome":
                amount_str = str(operation['amount'])
                amount = float(amount_str.replace(' ', '').replace(',', '.'))
                category_name = Category.objects.get(id=operation["categories"]).name

                if category_name not in data:
                    data[category_name] = {
                        'total': 0.0,
                        'operations': []
                    }

                data[category_name]['total'] += amount
                data[category_name]['operations'].append({
                    'date': operation["date"],
                    'amount': amount
                })
                total += amount

                for category, data in data.items():
                    for op in str(data['operations']):
                        operations.append({
                            'category': category,
                            'date': op['date'],
                            'amount': op['amount'],
                            '_raw_amount': op['amount']
                        })
            elif query == "targets":
                amount_str = str(operation['amount'])
                amount = float(amount_str.replace(' ', '').replace(',', '.'))
                target_name = Target.objects.get(id=operation["target"]).name

                if target_name not in data:
                    data[target_name] = {
                        'total': 0.0,
                        'operations': []
                    }

                data[target_name]['total'] += amount
                data[target_name]['operations'].append({
                    'date': operation["date"],
                    'amount': amount
                })
                total += amount

                for category, data in data.items():
                    for op in data['operations']:
                        operations.append({
                            'category': category,
                            'date': op['date'],
                            'amount': op['amount'],
                            '_raw_amount': op['amount']
                        })
                headers = ["Date", "Target", "Amount"]

        ws.merge_cells('A1:C1')
        title_cell = ws['A1']
        title_cell.value = "Freenance"
        title_cell.font = Font(bold=True, size=16)
        title_cell.alignment = Alignment(horizontal='center')


        ws.append(headers)

        header_style = Font(bold=True)
        amount_alignment = Alignment(horizontal='right', vertical='center')
        center_alignment = Alignment(horizontal='center', vertical='center')

        for col in range(1, 4):
            cell = ws.cell(row=2, column=col)
            cell.font = header_style
            cell.alignment = center_alignment

        start_data_row = 3
        for i, op in enumerate(operations, start=start_data_row):
            ws.cell(row=i, column=1, value=op['date']).alignment = center_alignment
            ws.cell(row=i, column=2, value=op['category'])
            amount_cell = ws.cell(row=i, column=3, value=op['amount'])
            amount_cell.number_format = '#,##0.00'
            amount_cell.alignment = amount_alignment

        total_row = len(operations) + start_data_row
        ws.cell(row=total_row, column=2, value="Итого:").font = header_style
        total_cell = ws.cell(row=total_row, column=3, value=total)
        total_cell.font = header_style
        total_cell.number_format = '#,##0.00'
        total_cell.alignment = amount_alignment

        for col_idx in range(1, 4):
            column_letter = get_column_letter(col_idx)
            max_length = 0
            for cell in ws.iter_cols(min_col=col_idx, max_col=col_idx):
                for c in cell:
                    try:
                        if not isinstance(c, MergedCell):
                            if len(str(c.value)) > max_length:
                                max_length = len(str(c.value))
                    except:
                        pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column_letter].width = adjusted_width

        pie_chart = PieChart()

        chart_data_row = total_row + 2
        ws.cell(row=chart_data_row, column=5, value="Category").font = header_style
        ws.cell(row=chart_data_row, column=6, value="Amount").font = header_style

        for i, (category, data) in enumerate(data.items(), start=chart_data_row + 1):
            ws.cell(row=i, column=5, value=category)
            ws.cell(row=i, column=6, value=total).number_format = '#,##0.00'

        data = Reference(ws,
                         min_col=6,
                         min_row=chart_data_row + 1,
                         max_row=chart_data_row + len(data))

        categories = Reference(ws,
                               min_col=5,
                               min_row=chart_data_row + 1,
                               max_row=chart_data_row + len(data))

        pie_chart.add_data(data, titles_from_data=False)
        pie_chart.set_categories(categories)
        pie_chart.title = "Categories"
        pie_chart.style = 10
        pie_chart.legend.position = 'r'

        ws.add_chart(pie_chart, "E2")

        wb.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="financial_report.xlsx"'
        return response

        # except Exception as e:
        #     return HttpResponse(
        #         f"Ошибка при создании отчёта: {str(e)}",
        #         status=500,
        #         content_type='text/plain')