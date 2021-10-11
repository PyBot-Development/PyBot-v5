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
  render() {
    return (
      <div className="Header">
        <header className="Header header">
          <p className="main-text">{this.props.text}</p>
          <div className="cheeseburgir">
            <HamburgerMenu
              isOpen={this.state.menuOpen}
              menuClicked={this.openMenu.bind(this)}
              width={32}
              height={24}
              strokeWidth={3}
              rotate={0}
              color='#b0b8c6'
              borderRadius={3}
              animationDuration={0.5}
              className="menu"
            />
            <CheeseburgerMenu isOpen={this.state.menuOpen} closeCallback={this.closeMenu.bind(this)}>
              <div className="menu-content">
                <div className="exit-button" style={{ display: "flex", float: "right" }} onClick={this.closeMenu.bind(this)}>
                  <Twemoji svg text="❌" />
                </div>
                <div className="menu-content-links">
                  <p style={{ textAlign: "center", fontSize: "calc(10px + 3vmin)" }}>Pages</p>
                  <ul>
                    <li key="Home">
                      <NavLink to="/home" onClick={this.closeMenu.bind(this)} activeClassName="selected">
                        <Twemoji svg text="🏠 Home" />
                      </NavLink>
                      <br />
                    </li>
                  </ul>
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