import React from 'react';

import { createMuiTheme, MuiThemeProvider } from 'material-ui/styles';

/* application components */
import Header from '../../components/Header';
import Navigation from '../../components/Navigation';
import { Footer } from '../../components/Footer';
import { Home } from '../../components/Home';

const theme = createMuiTheme({});

const styles = {
  root: {
    width: '100%',
    zIndex: 1,
    overflow: 'hidden',
  },
  appFrame: {
    position: 'relative',
    display: 'flex',
    width: '100%',
    height: '100%',
  },
  content: {
    width: '100%',
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: 24,
    height: 'calc(100% - 56px)',
    marginTop: 56,
    [theme.breakpoints.up('sm')]: {
      height: 'calc(100% - 64px)',
      marginTop: 64,
    },
  },
};

/* global styles for app */
import './styles/app.scss';

class App extends React.Component { // eslint-disable-line react/prefer-stateless-function
    static propTypes = {
        children: React.PropTypes.node,
    };

    render() {
        return (
            <MuiThemeProvider theme={theme}>
                <div style={styles.root}>
                <section style={styles.appFrame}>
                    <Header />
                    <Navigation />
                    <main style={styles.content}>
                        {this.props.children}
                    </main>
                    <Footer />
                </section>
                </div>
            </MuiThemeProvider>
        );
    }
}

export { App };
