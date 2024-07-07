// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import CreateEvent from './components/CreateEvent';
import EventList from './components/EventList';
import RegisterEvent from './components/RegisterEvent';
import EventRegistrations from './components/EventRegistrations';

const App = () => {
    return (
        <Router>
            <div>
                <Switch>
                    <Route path="/login" component={Login} />
                    <Route path="/register" component={Register} />
                    <Route path="/create-event" component={CreateEvent} />
                    <Route path="/events" component={EventList} exact />
                    <Route path="/events/:id/register" component={RegisterEvent} />
                    <Route path="/events/:id/registrations" component={EventRegistrations} />
                </Switch>
            </div>
        </Router>
    );
};

export default App;
