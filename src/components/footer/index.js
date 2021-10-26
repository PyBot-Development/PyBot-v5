import react from 'react'
import './index.sass'
import { SiGithub, SiYoutube, SiDiscord } from "react-icons/si";
class Footer extends react.Component {
  render() {
    return (
      <div className="bottom">
          <div className="footer">
            <a href="https://discord.gg/v3ATrV72B6" target="_blank" rel="noreferrer"> <SiDiscord></SiDiscord> </a>
            <a href="https://github.com/m2rsho" target="_blank" rel="noreferrer"> <SiGithub></SiGithub> </a>
            <a href="https://youtube.com/c/mariyt10" target="_blank" rel="noreferrer"> <SiYoutube></SiYoutube> </a>
          </div>
      </div>
    )
  }
}

export default Footer;