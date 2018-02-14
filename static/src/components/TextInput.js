import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Input, { InputLabel } from 'material-ui/Input';
import TextField from 'material-ui/TextField';
import { FormControl } from 'material-ui/Form';
import purple from 'material-ui/colors/purple';
import SnackBar from './SnackBar';
import ContentCopy from 'material-ui-icons/ContentCopy';
import Button from 'material-ui/Button';
import Badge from 'material-ui/Badge';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
  },
  inputInkbar: {
    '&:after': {
      backgroundColor: purple[500],
    },
  },
  textFieldRoot: {
    padding: 0,
    'label + &': {
      marginTop: theme.spacing.unit * 3,
    },
  },
  textFieldInput: {
    borderRadius: 4,
    backgroundColor: theme.palette.common.white,
    border: '1px solid #ced4da',
    fontSize: 16,
    padding: '10px 12px',
    width: 'calc(100% - 24px)',
    transition: theme.transitions.create(['border-color', 'box-shadow']),
    '&:focus': {
      borderColor: '#80bdff',
      boxShadow: '0 0 0 0.2rem rgba(0,123,255,.25)',
    },
  },
  textFieldFormLabel: {
    fontSize: 18,
  },
  button: {
    margin: theme.spacing.unit,
  },
  badgeRed: {
    color: 'white',
    backgroundColor: 'red'
  },
  badgeGreen: {
    color: 'white',
    backgroundColor: 'green'
  },
  badgeOrange: {
    color: 'white',
    backgroundColor: 'orange'
  },
});

function TextInput(props) {
  const { classes, section, type, label, 
        value, onChange, score, source } = props;

  let textInput = null;

  function copyToClipboard(e) {
      textInput.select()
      document.execCommand('copy')
  }

  return (
    <div className={classes.container}>
      <FormControl fullWidth className={classes.formControl}>
                                <Badge badgeContent={score + '%'}
                                classes={{
                                    badge: (score < 40 ? classes.badgeRed : 
                                    (score < 95 ? classes.badgeOrange : classes.badgeGreen))
                                }} color="inherit">

          <InputLabel htmlFor={'field' + section}
            shrink={true}
            classes={{
              root: classes.textFieldFormLabel,
            }}>{section.toUpperCase()} {label}</InputLabel>

          <Input
            id={'field' + section} value={value}
            inputRef={(input) => { textInput = input; }}
            disableUnderline={true}
            fullWidth={true}
            multiline={type === 'text' ? false : true }
            classes={{
              formControl: classes.textFieldInput,
            }}
          />

                                </Badge>
      </FormControl>
      <SnackBar message={source}/>
      {/* only displaying the button if the copy command exists */
        document.queryCommandSupported('copy') &&
        <Button variant="flat" mini={true} size="small" aria-label="add"
          aria-label="Copy to clipboard" onClick={copyToClipboard}>
          <ContentCopy />
          Copy
        </Button>
      }
    </div>
  );
}

TextInput.propTypes = {
  section: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  score: PropTypes.number.isRequired,
  value: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(TextInput);
