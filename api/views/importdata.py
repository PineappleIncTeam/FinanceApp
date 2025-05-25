from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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

from api.models import Operation, Category
from api.serializers import OperationSerializer


class OperationPDFView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OperationSerializer

    def get_queryset(self):
        queryset = Operation.objects.filter(user=self.request.user)

        operation_type = self.request.query_params.get('type')

        if operation_type:
            queryset = queryset.filter(type=operation_type)
        return queryset.select_related('categories').order_by('-created_at')

    @swagger_auto_schema(
        operation_id='Получение выписки в формате pdf',
        operation_description='Получение .pdf файла',
        manual_parameters=[
            openapi.Parameter(
                name="type",
                in_=openapi.IN_QUERY,
                description="Фильтр по типу операций",
                type=openapi.TYPE_STRING,
                enum=["targets", "outcome", "income"],
                required=True,
            ),
        ],
        responses = {
            200: openapi.Response(description="Файл успешно получен", schema=OperationSerializer),
    })
    def get(self, request):
        pdfmetrics.registerFont(TTFont('Bold', 'font/bold.ttf'))
        pdfmetrics.registerFont(TTFont('Regular', 'font/Regular.ttf'))
        operations = []
        total = 0.0
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        for operation in serializer.data:
            amount_str = str(operation['amount'])
            amount = float(amount_str.replace(' ', '').replace(',', '.'))
            total += amount

            formatted_amount = "{:,.2f}".format(amount).replace(",", " ")

            operations.append({
                "category": Category.objects.get(id=operation["categories"]).name,
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

            # Подготовка данных для таблицы
            table_data = [
                ["Date", "Category", "Amount"]  # Заголовки столбцов
            ]

            for op in operations:
                table_data.append([
                    op['date'],
                    op['category'],
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
        queryset = Operation.objects.filter(user=self.request.user)

        operation_type = self.request.query_params.get('type')

        if operation_type:
            queryset = queryset.filter(type=operation_type)
        return queryset.select_related('categories').order_by('-created_at')


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
        ],
        responses = {
            200: openapi.Response(description="Файл успешно получен", schema=OperationSerializer),
    })
    def get(self, request):
        operations = []
        total = 0.00
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        for operation in serializer.data:
            amount_str = str(operation['amount'])
            amount = float(amount_str.replace(' ', '').replace(',', '.'))
            total += amount

            formatted_amount = "{:,.2f}".format(amount).replace(",", " ")

            operations.append({
                "category": Category.objects.get(id=operation["categories"]).name,
                "amount": formatted_amount,
                "date": operation["date"],
                "_raw_amount": amount
            })

        try:
            buffer = BytesIO()
            wb = Workbook()
            ws = wb.active
            ws.title = "Freenance"

            ws['A1'] = "Freenance"
            ws['A1'].font = Font(bold=True, size=16)

            headers = ["Date", "Category", "Amount"]
            ws.append(headers)
            amount_alignment = Alignment(horizontal='right', vertical='center')

            header_alignment = Alignment(horizontal='center', vertical='center')
            for cell in ws[2]:
                cell.font = Font(bold=True)
                cell.alignment = header_alignment


            for op in operations:
                row = [op['date'], op['category'], op['amount']]
                ws.append(row)
                amount_cell = ws.cell(row=ws.max_row, column=3)
                amount_cell.number_format = '#,##0.00'
                amount_cell.alignment = amount_alignment

            for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=1, max_col=1):
                for cell in row:
                    cell.alignment = amount_alignment

            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                ws.column_dimensions[column_letter].width = adjusted_width
            total_row = ws.max_row + 1
            ws.cell(row=total_row, column=2, value="Total").font = Font(bold=True)
            total_cell = ws.cell(row=total_row, column=3, value=float(total))
            total_cell.font = Font(bold=True)
            total_cell.number_format = '#,##0.00'
            wb.save(buffer)
            buffer.seek(0)

            if buffer.getbuffer().nbytes < 100:
                raise ValueError("Generated Excel file is empty")

            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="financial_report.xlsx"'
            return response

        except Exception as e:
            return HttpResponse(
                f"Error generating Excel: {str(e)}",
                status=500,
                content_type='text/plain'
            )