


import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import ListSubheader from 'material-ui/List/ListSubheader';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Collapse from 'material-ui/transitions/Collapse';
import InboxIcon from 'material-ui-icons/MoveToInbox';
import DraftsIcon from 'material-ui-icons/Drafts';
import SendIcon from 'material-ui-icons/Send';
import ExpandLess from 'material-ui-icons/ExpandLess';
import ExpandMore from 'material-ui-icons/ExpandMore';
import StarBorder from 'material-ui-icons/StarBorder';
import Avatar from 'material-ui/Avatar';

const styles = theme => ({
  root: {
    width: '100%',
    maxWidth: 360,
    backgroundColor: theme.palette.background.paper,
  },
  nested: {
    paddingLeft: theme.spacing.unit * 4,
  },
  avatar: {
  },
  subsection: {
  },
  selectedsubsection: {
    backgroundColor: 'grey'
  },
  selectedavatar: {
    backgroundColor: 'green'
  },
});

class NestedList extends React.Component {
  state = { sections: [] };

  handleClick = (index) => {
    console.log(this.state);
    let sectionState = { open: !(this.state.sections[index] || { open: false }).open };
    let newSections = [...this.state.sections ];
    newSections[index] = sectionState
    this.setState({ ...this.state, ...{ sections: newSections }});
  };

  clickOnSection = (section, subSection, index, callBack) => {
    if (!subSection) {
      // Click on section
      this.handleClick(index)
    }
    callBack(section, subSection);
  };

  render() {
    const { classes, sections, subSections, selectedSection, selectedSubSection, callBack } = this.props;

    return (
      <div className={classes.root}>
        <List component="nav" subheader={<ListSubheader component="div">Sections</ListSubheader>}>
         {sections.map((section, index) => <div key={"listitem" + index}><ListItem button
            onClick={() => this.clickOnSection(section, null, index, callBack)}>
            <Avatar classes={{
              root: (selectedSection === section) ? classes.selectedavatar : classes.avatar
            }}>{section}</Avatar>
            <ListItemText inset primary={"Section "+ section} />
              {this.state.sections && this.state.sections[index] && this.state.sections[index].open ? <ExpandLess/> : <ExpandMore/>}
          </ListItem>
          {subSections[section] ? <Collapse in={this.state.sections && this.state.sections[index] && this.state.sections[index].open} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {subSections[section].map((subSection, index) => <ListItem button classes={{
                  root: (selectedSubSection === subSection) ? classes.selectedsubsection : classes.subsection
                  }} className={classes.nested} 
                  onClick={() => this.clickOnSection(section, subSection, index, callBack)} key={"sublistitem" + index}>
                  <ListItemText primary={subSection} />
                </ListItem>)}
              </List>
            </Collapse> : <span/>}
            </div>
          )}
        </List>
      </div>
    );
  }
}

NestedList.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(NestedList);