import react from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class HowTo extends react.Component {
  constructor() {
    super();
    this.state = {};
  }

  componentDidMount() {
    window.document.title = "How To? | Py-bot.cf"
  }

  render() {
    return (
      <div className="container" style={{ minHeight: "80vh", paddingTop: "15px" }}>
        Stuff Here
      </div>
    );
  }
}

export default HowTo;
