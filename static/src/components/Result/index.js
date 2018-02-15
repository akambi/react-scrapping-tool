/* eslint camelcase: 0, no-underscore-dangle: 0 */

import React, { Component } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import Button from 'material-ui/Button';
import Paper from 'material-ui/Paper';

import { withStyles } from 'material-ui/styles';
import TextInput from '../TextInput';
import * as actionCreators from '../../actions/auth';
import { CircularProgress } from 'material-ui/Progress';

import { validateEmail } from '../../utils/misc';
import { browserHistory } from 'react-router';

function mapStateToProps(state) {
    return {
        ...state.data.protocol_metas,
        section: state.data.selectedSection,
        subSection: state.data.selectedSubSection
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

const style = {
    paddingBottom: 35,
    paddingTop: 0,
    width: '100%',
    textAlign: 'center',
    display: 'inline-block',
    marginTop: 50,
    marginBottom: 50,
    overflow: scroll
};

const cstyles = theme => ({
  progress: {
    margin: `-${theme.spacing.unit * 3}px 0 0 -${theme.spacing.unit * 3}px`,
    position: 'absolute',
    left: '50%',
    top: '50%' 
  },  
});

/* component styles */
import { styles } from './styles.scss';

@connect(mapStateToProps, mapDispatchToProps)
class ResultView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            email: '',
            password: '',
            email_error_text: null,
            password_error_text: null,
            disabled: true,
        };
    }

    componentWillMount() {
        if (!this.props.name) {
            browserHistory.push('/load');
        }
    }

    isDisabled() {
        let email_is_valid = false;
        let password_is_valid = false;

        if (this.state.email === '') {
            this.setState({
                email_error_text: null,
            });
        } else if (validateEmail(this.state.email)) {
            email_is_valid = true;
            this.setState({
                email_error_text: null,
            });

        } else {
            this.setState({
                email_error_text: 'Sorry, this is not a valid email',
            });
        }

        if (this.state.password === '' || !this.state.password) {
            this.setState({
                password_error_text: null,
            });
        } else if (this.state.password.length >= 6) {
            password_is_valid = true;
            this.setState({
                password_error_text: null,
            });
        } else {
            this.setState({
                password_error_text: 'Your password must be at least 6 characters',
            });

        }

        if (email_is_valid && password_is_valid) {
            this.setState({
                disabled: false,
            });
        }

    }

    changeValue(e, type) {
        const value = e.target.value;
        const next_state = {};
        next_state[type] = value;
        this.setState(next_state, () => {
            this.isDisabled();
        });
    }

    _handleKeyPress(e) {
        if (e.key === 'Enter') {
            if (!this.state.disabled) {
                this.login(e);
            }
        }
    }

    login(e) {
        e.preventDefault();
        this.props.registerUser(this.state.email, this.state.password, this.state.redirectTo);
    }

    render() {
        const { classes } = this.props;


        console.log(this.props.subSection, this.props.data &&
                                this.props.data.protocoldata.filter(field => field.section === this.props.section), this.props.data &&
                                this.props.data.protocoldata.filter(field => field.section === this.props.section)
                                .filter(field => ((this.props.subSection === null) || (field.subSection === this.props.subSection))));

        return this.props.isFetching ? <CircularProgress className={classes.progress} size={50} />  : !this.props.loaded ? <span/> : (

            <div className={`container-fluid ${styles}`}>
                <div className="col-md-12" onKeyPress={(e) => this._handleKeyPress(e)}>
                    <Paper style={style}>
                        {this.props.isFetching ? <span/> : 
                        <div>
                            <h3>Protocol - {this.props.name.replace(/\.[^/.]+$/, "")}</h3>
                            {
                                this.props.data &&
                                this.props.data.protocoldata.filter(field => field.section === this.props.section)
                                .filter(field => ((this.props.subSection === null) || (field.subSection === this.props.subSection)))
                                .map((field, index) => <div key={field.id + index} className="col-md-12">
                                  <TextInput
                                  section={field.id}
                                  label={field.eudractlabel}
                                  value={field.value}
                                  type={field.type}
                                  score={field.score}
                                  onChange={(e) => this.changeValue(e, field.id)}
                                  source={field.raw_text}
                                  />
                            </div>)
                            }
                        </div>
                        }
                    </Paper>

                </div>
            </div>
        );

    }
}

ResultView.propTypes = {
    name: React.PropTypes.string,
    data: React.PropTypes.object,
    isFetching: React.PropTypes.bool,
    loaded: React.PropTypes.bool,
    classes: React.PropTypes.object.isRequired,
    section: React.PropTypes.string,
};

export default withStyles(cstyles, { withTheme: true })(ResultView);
