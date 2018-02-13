import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
/*import InboxIcon from 'material-ui-icons/Inbox';
import DraftsIcon from 'material-ui-icons/Drafts';
import SectionIcon from 'material-ui-icons/label';*/
import Avatar from 'material-ui/Avatar';


export const sectionListItems = <List component="nav">
       {["A","B","C"].map ((section) => <ListItem button>
          <Avatar>{section}</Avatar>
          <ListItemText primary={"Section "+ section} />
        </ListItem>)}
      </List>;


