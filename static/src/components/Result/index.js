/* eslint camelcase: 0, no-underscore-dangle: 0 */

import React, { Component } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import Button from 'material-ui/Button';
import Paper from 'material-ui/Paper';

import { withStyles } from 'material-ui/styles';
import TextInput from '../TextInput';

import { changeFieldValue } from '../../actions/data';
const actionCreators = { changeFieldValue };

import LoaderView from '../Loader';
import { browserHistory } from 'react-router';

function mapStateToProps(state) {
    return {
        ...state.data.protocol_metas,
        section: state.data.selectedSection,
        subSection: state.data.selectedSubSection,
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

    changeValue(e, type) {
        this.props.changeFieldValue(type, e.target.value);
    }

    render() {
        const { classes, isFetching } = this.props;

        return this.props.isFetching ? <LoaderView isFetching={this.props.isFetching}/>  : !this.props.loaded ? <span/> : (

            <div className={`container-fluid ${styles}`}>
                <div className="col-md-12">
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
