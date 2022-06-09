import React from 'react'

function Button({ type, title, disable, onClick, className }) {
  return (
    <input type={"button"} value={title} onClick={onClick} className={className}></input>
  )
}

export default Button