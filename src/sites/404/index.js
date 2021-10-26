import react from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Snackbar, Alert } from '@mui/material'

class NotFound extends react.Component {
    constructor(props) {
        super(props)

        this.state = {
            open: false,
        }
    }

    handleClose() {
        this.setState({ open: false })
        window.location = "/"
    }
    handleClick() {
        this.setState({ open: true })
        window.location = "/"
    }

    render() {

        return (
            <div className="d-flex p-2 justify-content-center" style={{ minHeight: "100vh" }}>
                <div style={{ textAlign: "center", justifyContent: "center", margin: "auto" }}>
                    <h1 style={{fontWeight: "200"}}>Error <span style={{color: "$B85C38"}}>404</span></h1>
                    <p>Not Found</p>
                    <Button onClick={this.handleClick.bind(this)} variant="outlined">Go Back</Button>
                </div>
                <Snackbar open={this.state.open} autoHideDuration={6000} onClose={this.handleClose.bind(this)}>
                    <Alert onClose={this.handleClose.bind(this)} severity="info" sx={{ width: '100%' }}>
                        Redirecting
                    </Alert>
                </Snackbar>
            </div>
        )
    }
}

export default NotFound;
