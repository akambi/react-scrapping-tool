import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemIcon, ListItemText, ListSubheader } from 'material-ui/List';
import Avatar from 'material-ui/Avatar';

export const clickOnSection = (section, callBack) => {
  callBack(section);
};

export const sectionListItems = (sections, callBack) => <List component="nav" subheader={<ListSubheader component="div">Sections</ListSubheader>}>
       {sections.map((section, index) => <ListItem button key={"listitem" + index}
          onClick={() => clickOnSection(section, callBack)}>
          <Avatar>{section}</Avatar>
          <ListItemText primary={"Section "+ section} />
        </ListItem>)}
      </List>;


