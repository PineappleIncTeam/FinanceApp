import MainFieldString from './MainFieldString';

function MainField() {
  const oneTime = ['Временные', 'Подработка', 'Наследство', 'Добавить категорию'];
  const permanent = [
    'Постоянные',
    'Зарплата',
    'Подработка',
    'Планируемые',
    'Добавить категорию',
  ];

  return (
    <div className="main_field" key="">
      <h2 className="main_field_title">Доходы</h2>
      <input className="input_rub"></input>
      <MainFieldString type={permanent} />
      <MainFieldString type={oneTime} />
    </div>
  );
}

export default MainField;
