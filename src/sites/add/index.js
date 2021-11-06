import react from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class HowTo extends react.Component {
  constructor() {
    super();
    this.state = {};
  }

  componentDidMount() {
    window.document.title = "Add | Py-bot.cf"
  }

  render() {
    return (
      <div className="container" style={{ minHeight: "80vh", paddingTop: "15px" }}>
        <a href="https://discord.com/oauth2/authorize?client_id=885631013844291674&permissions=67420224&scope=bot%20applications.commands" target="_blank" rel="noreferrer" >Add Link</a>
      </div>
    );
  }
}

export default HowTo;
