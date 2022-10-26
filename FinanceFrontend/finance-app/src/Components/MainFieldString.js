import SelectElement from './SelectElement';

function MainFieldString(props) {
  
  return (
    <form action="" method="post" className="main_field_string">
      <SelectElement type={props.type} />
      <input type="text" className="main_field_string_input"></input>
      <button type="submit" className="main_field_string_button">Добавить</button>
    </form>
  );
}
export default MainFieldString;
