import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import {Route,BrowserRouter as Router, Switch} from 'react-router-dom';
import './index.css';
import App from './App';
import Header from './components/header';
import Register from './components/register';
import Login from './components/login';


const routing = (
    <Router>
        <React.StrictMode>
            <Header />
            <Switch>
                <Route exact path="/" component={App} />
                <Route path="/register" component={Register} />
				        <Route path="/login" component={Login} />
            </Switch>
        </React.StrictMode>
    </Router>
);

ReactDOM.render(routing,document.getElementById('root'));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
