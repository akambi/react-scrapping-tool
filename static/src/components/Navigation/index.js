import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Drawer from 'material-ui/Drawer';
import List from 'material-ui/List';
import Divider from 'material-ui/Divider';
import IconButton from 'material-ui/IconButton';
import ChevronLeftIcon from 'material-ui-icons/ChevronLeft';
import ChevronRightIcon from 'material-ui-icons/ChevronRight';
import { sectionListItems } from './sections';

import { logoutAndRedirect } from '../../actions/auth';
import { openMenu, closeMenu, selectSection } from '../../actions/data';

import { drawerWidth } from '../../constants/index';

const actionCreators = { logoutAndRedirect, openMenu, closeMenu, selectSection };

const styles = theme => ({
  drawerPaper: {
    position: 'relative',
    height: '100%',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    width: 66,
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  drawerInner: {
    // Make the items inside not wrap when transitioning:
    width: drawerWidth,
  },
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
});

function mapStateToProps(state) {
    let sections = [];
    if (state.data.protocol_metas && state.data.protocol_metas.data) {
      sections = [...new Set(state.data.protocol_metas.data.protocoldata.map(item => item.section))]
    }

    return {
        isNavMenuOpened: state.data.openedMenu,
        sections: sections,
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
class Navigation extends Component {
    constructor(props) {
        super(props);
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.sections.length && nextProps.sections[0] != this.props.sections[0]) {
          this.props.selectSection(this.props.sections[0]);
        }
    }

    handleDrawerClose = () => {
        this.props.closeMenu();
    };

    logout(e) {
        e.preventDefault();
        this.props.logoutAndRedirect();
        this.handleDrawerClose();
    }

    render() {
        const { classes, theme } = this.props;

        return (
          this.props.sections && this.props.sections.length ? 
          <Drawer
              variant="permanent"
              classes={{
                paper: classNames(classes.drawerPaper, !this.props.isNavMenuOpened && classes.drawerPaperClose),
              }}
              open={this.props.isNavMenuOpened}
            >                
              <div className={classes.drawerInner}>
                <div className={classes.drawerHeader}>
                  <IconButton onClick={this.handleDrawerClose}>
                    {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
                  </IconButton>
                </div>
                <Divider />
                <List className={classes.list}>{sectionListItems(this.props.sections, this.props.selectSection)}</List>
              </div>
          </Drawer> : <span/>
        );
    }
}

Navigation.propTypes = {
    logoutAndRedirect: React.PropTypes.func,
    isNavMenuOpened: React.PropTypes.bool,
    sections: React.PropTypes.array
};

export default withStyles(styles, { withTheme: true })(Navigation);
