/* eslint new-cap: 0 */

import React from 'react';
import { Route } from 'react-router';

/* containers */
import { App } from './containers/App';
import ResultView from './components/Result';
import LoginView from './components/LoginView';
import RegisterView from './components/RegisterView';
import { Home } from './components/Home';
import Analytics from './components/Analytics';
import NotFound from './components/NotFound';

import { DetermineAuth } from './components/DetermineAuth';
import { requireAuthentication } from './components/AuthenticatedComponent';
import { requireNoAuthentication } from './components/notAuthenticatedComponent';

export default (
    <Route path="/" component={App}>
        <Route path="login" component={requireNoAuthentication(LoginView)} />
        <Route path="register" component={requireNoAuthentication(RegisterView)} />
        <Route path="load" component={requireAuthentication(Home)} />
        <Route path="result" component={requireAuthentication(ResultView)} />
        <Route path="analytics" component={requireAuthentication(Analytics)} />
        <Route path="*" component={DetermineAuth(NotFound)} />
    </Route>
);
