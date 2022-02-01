import react from "react";
import "bootstrap/dist/css/bootstrap.min.css";

class Pp extends react.Component {
  render() {
    window.document.title = "Terms Of Service | Py-bot.cf";
    return (
      <>
        <div
          className="container"
          style={{ minHeight: "80vh", paddingTop: "15px" }}
        >
          <h1>Privacy Policy</h1>
          <p>
            To provide our services we need to collect some data from our users.
            Data that isn't relevant to our services is never collected and
            stored. We assume that every user has read and agreed to this
            policy.
          </p>

          <h2>Collected data</h2>
          <p>
            To provide our services we need to collect and store user data
            provided by discord. This may include your discord user id, name,
            discriminator and avatar. Beside these information, we are only
            storing data that is directly provided by the user. This may include
            message data, and uploaded files.
          </p>

          <h2>Data protection</h2>
          <p>
            We ensure all users that their data is securely stored. Our site
            complies with the requirements of the European Union to protect the
            client data (GDPR).
          </p>

          <h2>User Responsibility</h2>
          <p>
            The user is responsible for their data on this site. They should not
            share any sensitive or inappropriate information over our services.
            We advice our users to not share any information that they wouldn't
            want to be public.
          </p>

          <h2>Modification rights</h2>
          <p>
            Please be aware that information on this page might change at any
            time. Specific items might be deleted, modified or added. We
            therefore ask you to keep an eye out for changes yourself.
          </p>

          <h2>Data deletion</h2>
          <p>
            Every user has the right to request or delete all of their data at
            any point. Under certain circumstances it may take up to 30 days for
            us to delete or provide the requested the data. You can request your
            data by email: mariyt.contact@gmail.com
          </p>
        </div>
      </>
    );
  }
}

export default Pp;
