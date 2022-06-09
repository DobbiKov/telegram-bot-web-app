import { useState, useEffect, useMemo } from "react";
import styles from "./App.module.css"
import Button from "./components/Button/Button";
import Input from "./components/Input/Input";
import logo from "./img/Logo-02.png"


const tele = window.Telegram.WebApp;
let dataMain = 0;



function App() {
  const [inputData, setInputData] = useState({
    name: "", email: "", discord: "", nickname: "", age: ""
  })
  const [isInputFinished, setIsInputFinished] = useState(false);
  const [hideFinishButton, setHideFinishButton] = useState(true); //have to be true!!!!

  const onChange = (e) => {
    setInputData({...inputData, [e.target.name]: e.target.value})
    // console.log(inputData)
    dataMain = inputData;
    if(
      inputData.name.length > 2 &&
      inputData.email.length > 5 &&
      inputData.discord.length > 6 &&
      inputData.age.length >= 1
    )
    {
      // tele.MainButton.text = "Подати заявку";
      // tele.MainButton.show();
      setHideFinishButton(false);

      // window.Telegram.WebApp.onEvent('mainButtonClicked', function(){
      //   // tele.sendData(`${inputData}`); 
      //   tele.sendData(`${inputData.name},${inputData.email},${inputData.discord},${inputData.nickname},${inputData.age}`); 
      // });
    }
    else tele.MainButton.hide();
  }
  useEffect(() => {
    tele.ready();
    // window.Telegram.WebApp.offEvent('mainButtonClicked', function(){});

    // window.Telegram.WebApp.onEvent('mainButtonClicked', function(){
    //   // tele.sendData("some string that we need to send"); 
    //   // tele.sendData(`${inputData}`); 
    //   tele.sendData(`${inputData.name},${inputData.email},${inputData.discord},${inputData.nickname},${inputData.age}`); 
    //   // dataMain = 1;
    //   //при клике на основную кнопку отправляем данные в строковом виде
    // });
  });
  function getClassorHide(className, isHide)
  {
    if(isHide
      ) return styles.hideBlock;
    return className;
  }
  const onButtonClick = (e) => {
    // console.log("fdsa")
    setIsInputFinished(true);

    tele.MainButton.text = "Надіслати заявку";
    tele.MainButton.show();

    window.Telegram.WebApp.onEvent('mainButtonClicked', function(){
      // tele.sendData(`${inputData}`); 
      // tele.sendData(`${inputData.name},${inputData.email},${inputData.discord},${inputData.nickname},${inputData.age}`); 
      tele.sendData(JSON.stringify(inputData)); 
    });
  }
  return (
    <div className={styles.app}>
      <div className={styles.imageWrapper}>
        <img src={logo} className={styles.logo}></img>
      </div>
      <div className={styles.titleDiv}>
        <h1 className={styles.title}>Заявка на ЗБТ</h1>
        {/* <h1 className={styles.title}></h1> */}
      </div>
      <div className={getClassorHide(styles.inputsWrapper, isInputFinished)}>
        <div className={styles.inputs}>
          <Input onChange={onChange} type={"text"} setInputData={setInputData} inputData={inputData} title={"Ім'я"} id={"name"}></Input>
          <Input onChange={onChange} type={"email"} setInputData={setInputData} inputData={inputData} title={"Email"} id={"email"}></Input>
          <Input onChange={onChange} type={"text"} setInputData={setInputData} inputData={inputData} title={"Discord"} id={"discord"}></Input>
          <Input onChange={onChange} type={"text"} setInputData={setInputData} inputData={inputData} title={"Нікнейм"} id={"nickname"}></Input>
          <Input onChange={onChange} type={"text"} setInputData={setInputData} inputData={inputData} title={"Вік"} id={"age"}></Input>
          {/* <button onClick={() => {console.log(inputData)}}>fdsa</button> */}
        </div>
      </div>
      <div className={getClassorHide(styles.buttonWrapper, isInputFinished)}>
        <Button title={"Завершити заповнення"} onClick={onButtonClick} className={getClassorHide(styles.button, hideFinishButton)}/>
      </div>
      <div className={getClassorHide(styles.lastTextWrapper, !isInputFinished)}>
        <div className={styles.lastTextBox}>
          <p className={styles.lastText}>Дякуємо за заповнення заявки! Натисніть кнопку <span className={styles.lastTextSend}>Надіслати заявку</span> та чекайте будь ласка на нашу відповідь. Слава Україні!</p>
        </div>
      </div>
    </div>
  );
}

export default App;
