import React from 'react';
import ReactDOM from 'react-dom';
import './index.sass';
import Routes from './router'

ReactDOM.render(
  <React.StrictMode>
    <Routes />
  </React.StrictMode>,
  document.getElementById('root')
);

