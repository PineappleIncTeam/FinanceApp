import Button from "./Button";
function ButtonNaviBlock() {
  const buttonName = ['Доходы', 'Расходы', 'Накопления', 'Аналитика'];

  return <div className="button_navi_block">
    {buttonName.map((text, index) => {
        return <Button text={text} key={index} />
    })}
  </div>
    
  

}

export default ButtonNaviBlock;
