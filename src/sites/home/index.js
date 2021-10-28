import react from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import delta from './assets/delta.webp'
import pybots from './assets/pybots.png'

const textArray = ['​Ἄ', '​Ɓ', '​С', '​Đ', '​Ӗ', '​Ϝ', '​Ɠ', '​Ң', '​ǐ', '​Ĵ', '​К', '​Ḽ', '​Μ', '​Ñ', '​Ṍ', '​Р', '​Ԛ', '​Ř', '​Ṣ', '​Ţ', '​Ǘ', '​Ṽ', '​Ẇ', '​Ẍ', '​Ƴ', '​Ẑ'];

class Home extends react.Component {
  constructor() {
    super();
    this.state = { textIdx: 0 };
  }

  componentDidMount() {
    window.document.title = "Home | Py-bot.cf"

    this.timeout = setInterval(() => {
      let currentIdx = this.state.textIdx;
      this.setState({ textIdx: currentIdx + 1 });
    }, 10);
  }

  render() {
    let text = ""
    for (var i = 0; i < 18; i++) {
      text = text.concat(textArray[Math.floor(Math.random() * this.state.textIdx) % textArray.length])
    }

    return (
      <div className="container" style={{ minHeight: "80vh", paddingTop: "15px" }}>
        <h1 style={{ textAlign: "center", fontWeight: "200" }}>
          Hello Cruel World!
        </h1>
        
        <div className="ad">
          <a href="https://discord.gg/dfKMTx9Eea" target="_blank" rel="noreferrer">
            <img className="discord" src={pybots} alt="pybot" style={{ height: "3em" }} /> Pybot's Discord Server
          </a> 
        </div>

        <div className="ad">
          <a href="https://discord.gg/2nxsWSHdKy" target="_blank" rel="noreferrer">
            <img className="discord" src={delta} alt="delta" style={{ height: "3em" }} /> oH yOu DoN't KnOw wHaT dElTa iS? It's {text}.
          </a> 
        </div>

        <p>

        </p>
      </div>
    );
  }
}

export default Home;
