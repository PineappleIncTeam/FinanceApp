import SelectElement from './SelectElement';

function MainFieldString(type) {
  
  return (
    <div className="main_field_string">
      <SelectElement type={type} />
      <input className="main_field_string_input"></input>
      <button className="main_field_string_button">Добавить</button>
    </div>
  );
}
export default MainFieldString;
