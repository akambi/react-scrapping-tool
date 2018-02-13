import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Button from 'material-ui/Button';
import Icon from 'material-ui/Icon';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import List from 'material-ui/List';
import Typography from 'material-ui/Typography';
import Divider from 'material-ui/Divider';
import IconButton from 'material-ui/IconButton';
import AccountCircle from 'material-ui-icons/AccountCircle';
import MenuIcon from 'material-ui-icons/Menu';
import ChevronLeftIcon from 'material-ui-icons/ChevronLeft';
import ChevronRightIcon from 'material-ui-icons/ChevronRight';
import SvgIcon from 'material-ui/SvgIcon';

import { logoutAndRedirect } from '../../actions/auth';
import { openMenu, closeMenu } from '../../actions/data';

import { drawerWidth } from '../../constants/index';

const actionCreators = { logoutAndRedirect, openMenu, closeMenu };

const HomeIcon = props => (
  <SvgIcon {...props}>
    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
  </SvgIcon>
);

const styles = theme => ({
  root: {
    width: '100%',
    height: 430,
    marginTop: theme.spacing.unit * 3,
    zIndex: 1,
    overflow: 'hidden',
  },
  appFrame: {
    position: 'relative',
    display: 'flex',
    width: '100%',
    height: '100%',
  },
  appBar: {
    position: 'absolute',
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 36,
  },
  hide: {
    display: 'none',
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
  header: { top: 0 },
  flex: {
    flex: 1,
  },
  leftIcon: {
    marginRight: theme.spacing.unit,
  },
});

function mapStateToProps(state) {
    let sections = [];
    if (state.data.protocol_metas && state.data.protocol_metas.data) {
      sections = [...new Set(state.data.protocol_metas.data.protocoldata.map(item => item.section))]
    }

    return {
        token: state.auth.token,
        isAuthenticated: state.auth.isAuthenticated,
        isNavMenuOpened: state.data.openedMenu,
        sections: sections,
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
class Header extends Component {
    constructor(props) {
        super(props);
    }

    dispatchNewRoute(route) {
        browserHistory.push(route);
        this.props.closeMenu();
    }

    logout(e) {
        e.preventDefault();
        this.props.logoutAndRedirect();
        this.props.closeMenu();
    }

    openNav(e) {
        this.props.openMenu();
    }

    render() {
        const { classes, theme } = this.props;

        return (
                    <AppBar color="primary" position="fixed" className={classNames(classes.header, classes.appBar, this.props.isNavMenuOpened && classes.appBarShift)}>
                        <Toolbar disableGutters={!this.props.isNavMenuOpened}>
                          {this.props.sections && this.props.sections.length ? <IconButton
                            color="inherit"
                            aria-label="open drawer"
                            onClick={(e) => this.openNav(e)}
                            className={classNames(classes.menuButton, this.props.isNavMenuOpened && classes.hide)}
                          >
                            <MenuIcon />
                          </IconButton> : <span className={classNames(classes.menuButton)}/>}

                        <Typography variant="title" color="inherit" className={classes.flex} style={{ lineHeight: 'normal' }}>
                            <div>
                                <div style={{ marginTop: 10 }}>CAPS vj7.1</div>
                                <div style={{ fontSize: 'small', fontWeight: 300 }}>Clinical protocol Scrapper</div>
                            </div>
                        </Typography>

                        <div>
                            {
                                !this.props.isAuthenticated ?
                                    <div>
                                        <Button
                                          onClick={() => this.dispatchNewRoute('/login')}
                                          color="inherit"
                                        >Login <AccountCircle className={classes.leftIcon}/></Button>
                                        <Button
                                          onClick={() => this.dispatchNewRoute('/register')}
                                          icon={<Icon className="material-icons"></Icon>}
                                          color="inherit"
                                        >Register</Button>
                                    </div>
                                    :
                                    <div>
                                        <Button
                                         onClick={() => this.dispatchNewRoute('/')}
                                         color="inherit">
                                            <HomeIcon className={classes.leftIcon}/> Load
                                         </Button>
                                        <Button
                                          onClick={(e) => this.logout(e)}
                                          color="inherit"
                                        ><Icon className="material-icons" />Logout</Button>
                                    </div>
                                }                        
                        </div>                              
                    </Toolbar>
                  </AppBar>
        );
    }
}

Header.propTypes = {
    logoutAndRedirect: React.PropTypes.func,
    isAuthenticated: React.PropTypes.bool,
    userName: React.PropTypes.string,
    token: React.PropTypes.string,
};

export default withStyles(styles, { withTheme: true })(Header);
