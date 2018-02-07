/* eslint camelcase: 0, no-underscore-dangle: 0 */

import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';

import * as actionCreators from '../actions/auth';

import { validateEmail } from '../utils/misc';

function mapStateToProps(state) {
    return {
        ...state.data.protocol_metas
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

const style = {
    marginTop: 15,
    paddingBottom: 35,
    paddingTop: 0,
    width: '100%',
    textAlign: 'center',
    display: 'inline-block',
};

@connect(mapStateToProps, mapDispatchToProps)
export default class ResultView extends React.Component {

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
        return !(this.props.isFetching || this.props.loaded) ? <span/> : (
            <div className="col-md-12" onKeyPress={(e) => this._handleKeyPress(e)}>
                <Paper style={style}>
                    {this.props.isFetching ? <span/> : 
                    <div className="text-center">
                        <h2>Metas get from protocol!</h2>

                        {
                            this.props.data && this.props.data.protocoldata.map((field) => <div key={field.id} className="col-md-12">
                            <TextField
                              hintText={field.id}
                              floatingLabelText={field.id}
                              type="text"
                              value={field.value}
                              errorText={this.state.email_error_text}
                              onChange={(e) => this.changeValue(e, 'email')}
                            />
                        </div>)
                        }
                        
                        <RaisedButton
                          disabled={this.state.disabled}
                          style={{ marginTop: 50 }}
                          label="Submit"
                          onClick={(e) => this.login(e)}
                        />

                    </div>
                    }
                </Paper>

            </div>
        );

    }
}

ResultView.propTypes = {
    name: React.PropTypes.string,
    data: React.PropTypes.object,
    isFetching: React.PropTypes.bool,
    loaded: React.PropTypes.bool,
};
