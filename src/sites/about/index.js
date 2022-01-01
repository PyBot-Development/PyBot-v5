import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function About() {
  window.document.title = "About | Py-bot.cf"
  return (
    <div className="container" style={{ minHeight: "80vh", paddingTop: "15px" }}>
      <h1 style={{ textAlign: "center", fontWeight: "200" }}>
        Info about Pybot
      </h1>

      <p>
        Under Construction
      </p>
    </div>
  );
}

export default About;
