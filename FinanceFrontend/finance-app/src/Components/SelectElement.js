function SelectElement(props) {
  //   const oneTime = [
  //     'Временные',
  //     'Подработка',
  //     'Наследство',
  //     'Добавить категорию',
  //   ];
  //   const permanent = [
  //     'Постоянные',
  //     'Зарплата',
  //     'Подработка',
  //     'Планируемые',
  //     'Добавить категорию',
  //   ];
  return (
    <select className="select_element">
      {props.type.map((text, index) => {
        return (
          <option className="option_list" key={index}>
            {text}
          </option>
        );
      })}
    </select>
  );
}
export default SelectElement;
