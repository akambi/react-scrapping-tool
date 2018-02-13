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

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
  },
  inputLabelFocused: {
    color: purple[500],
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
});

function TextInput(props) {
  const { classes, section, label, value, onChange, source } = props;

  let textInput = null;

  function copyToClipboard(e) {
      textInput.select()
      document.execCommand('copy')
  }

  return (
    <div className={classes.container}>
      <FormControl className={classes.formControl}>
        <InputLabel
          FormControlClasses={{
            focused: classes.inputLabelFocused,
          }}
          htmlFor="custom-color-input"
        >
          {section}
        </InputLabel>
        <Input
          classes={{
            inkbar: classes.inputInkbar,
          }}
          id="custom-color-input"
        />
      </FormControl>
      <TextField
        label={label}
        value={value}
        inputRef={(input) => { textInput = input; }}
        InputProps={{
          disableUnderline: true,
          classes: {
            root: classes.textFieldRoot,
            input: classes.textFieldInput,
          },
        }}
        InputLabelProps={{
          shrink: true,
          className: classes.textFieldFormLabel,
        }}
      />
      <SnackBar message={source}/>
      {/* only displaying the button if the copy command exists */
        document.queryCommandSupported('copy') &&
        <Button variant="fab" aria-label="add" className={classes.button} aria-label="Copy to clipboard" onClick={copyToClipboard}>
          <ContentCopy />
        </Button>
      }
    </div>
  );
}

TextInput.propTypes = {
  section: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(TextInput);
