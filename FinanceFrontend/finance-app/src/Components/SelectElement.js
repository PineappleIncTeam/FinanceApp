function SelectElement(type) {
  const oneTime = ['Подработка', 'Наследство', 'Добавить категорию']
    const permanent = [
    'Постоянные',
    'Зарплата',
    'Подработка',
    'Планируемые',
    'Добавить категорию',
  ];
  return (
    <select className="select_element">
      {permanent.map((text, index) => {
        return <option className="option_list" key={index}>{text}</option>
      })}
      
    </select>
  );
}
export default SelectElement;
