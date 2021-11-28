import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Collapsible from 'react-collapsible';
import './index.sass'

import { createTheme, ThemeProvider } from '@mui/material/styles';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

const commands = require('./commands.json')

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function Commands() {
  window.document.title = "Commands | Py-bot.cf"
  const [value, setValue] = React.useState('');
  const [openValue, setOpenValue] = React.useState('');

  var newState = {};

  function scroll(location) {
    newState[location] = true
    setOpenValue(newState)
    window.location = `#${location}`
  }

  const commandsDiv = []
  for (const item in commands.all) {
    newState[commands.all[item].label] = false
    commandsDiv.push(
      <div id={commands.all[item].label} key={commands.all[item].label} >
        <Collapsible
          triggerTagName="div"
          transitionTime={200}
          trigger={commands.all[item].label}
          open={openValue[commands.all[item].label]}
        >

          <h4 className="description">{commands.all[item].description}</h4>

          <p className="usage">Usage</p>
          <pre className="pre">{commands.all[item].usage}</pre>

          <p className="aliases">Aliases</p>
          <pre className="pre">{commands.all[item].aliases}</pre>

        </Collapsible>
      </div>)
  }

  const opCommandsDiv = []
  for (const item in commands.admin) {
    newState[commands.admin[item].label] = false
    opCommandsDiv.push(
      <div id={commands.admin[item].label} key={commands.admin[item].label} >
        <Collapsible
          triggerTagName="div"
          transitionTime={200}
          trigger={commands.admin[item].label}
          open={openValue[commands.admin[item].label]}
        >

          <h4 className="description">{commands.admin[item].description}</h4>

          <p className="usage">Usage</p>
          <pre className="pre">{commands.admin[item].usage}</pre>

          <p className="aliases">Aliases</p>
          <pre className="pre">{commands.admin[item].aliases}</pre>

        </Collapsible>
      </div>)
  }

  return (
    <div className="container" style={{ minHeight: "80vh", paddingTop: "15px" }}>
      <div className="search-text">
        <h1 style={{ textAlign: "left", fontWeight: "200" }}>
          Pybot's Commands
        </h1>
        <ThemeProvider theme={theme}>
        <Autocomplete
          
          value={value}
          onChange={(event, newValue) => {
            (newValue === null) ? void (0) : scroll(newValue.label)
            setValue(newValue);
          }}

          disablePortal
          id="search"
          options={commands.all.concat(commands.admin)}
          sx={{ width: 300, color: "#E0C097" }}
          renderInput={(params) => <TextField {...params} label="Search" />}
        />
        </ThemeProvider>
      </div>

      <div style={{ paddingTop: "25px" }}>
        {commandsDiv}
      </div>

      <h2 style={{ textAlign: "center", fontWeight: "200" }}>
          Op Commands (Require OP permissions)
      </h2>
      <div style={{ paddingTop: "25px" }}>
        {opCommandsDiv}
      </div>

    </div>
  );
}

export default Commands;
