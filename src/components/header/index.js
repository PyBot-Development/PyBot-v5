import { Twemoji } from 'react-emoji-render';
import CheeseburgerMenu from 'cheeseburger-menu'
import HamburgerMenu from 'react-hamburger-menu'
import react from 'react'
import { NavLink } from 'react-router-dom';
import './index.sass'

class Header extends react.Component {
  constructor(props) {
    super(props)

    this.state = {
      menuOpen: false,
    }
  }

  openMenu() {
    this.setState({ menuOpen: true })
  }

  closeMenu() {
    this.setState({ menuOpen: false })
  }

  createEntry(key, name, location){
    return(
      <div key={key} style={{borderTop: "solid 1px #E0C097", borderWidth: "100%"}}>
      <NavLink to={location} onClick={this.closeMenu.bind(this)} activeClassName="selected">
        <Twemoji svg text={name} />
      </NavLink>
      </div>
    )
  }

  render() {
    return (
      <div className="Header">
        <header className="Header header">
          <p className="main-text"><Twemoji text={this.props.text} /></p>
          <div className="cheeseburgir">
            <HamburgerMenu
              isOpen={this.state.menuOpen}
              menuClicked={this.openMenu.bind(this)}
              width={32}
              height={24}
              strokeWidth={3}
              rotate={0}
              color='#E0C097'
              borderRadius={3}
              animationDuration={0.5}
              className="menu"
            />
            <CheeseburgerMenu isOpen={this.state.menuOpen} closeCallback={this.closeMenu.bind(this)}>
              <div className="menu-content">
                <div className="menu-content-links">
                  <p style={{ textAlign: "center", fontSize: "calc(10px + 3vmin)" }}>Pages</p>


                  {this.createEntry("home", "🏡 Home", "/home")}
                  {this.createEntry("about", "🤔 About", "/about")}
                  {this.createEntry("changelog", "🖨️ Changelog", "/changelog")}
                  {this.createEntry("commands", "💾 Commands", "/commands")}
                  {this.createEntry("add", "➕ Add", "/add")}
                  {this.createEntry("terms-of-service", "📜 Terms Of Service", "/terms-of-service")}

                </div>
              </div>
            </CheeseburgerMenu>
          </div>
        </header>
      </div>
    )
  }
}

export default Header;
