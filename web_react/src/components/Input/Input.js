import React from 'react';
import styles from "./Input.module.css"

function Input({className, title, disable, setInputData, inputData, type, id, onChange}) {
  return (
    <div className={styles.inputWrapper}>
        <input 
        type={type} 
        onChange={onChange}
        className={styles.input}
        id={id}
        name={id}
        placeholder={" "}
        autoComplete={"off"}></input>
        <label 
        for={id}
        className={styles.label}>{title}</label>
    </div>
  )
}

export default Input;