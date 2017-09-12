/**
 * Created by chenkang1 on 2017/8/21.
 */

import React from "react";
import {connect} from 'dva';
import {Spin, Button } from 'antd';
import {fetchAndNotification} from "../../services/restfulService";
import styles from './index.less'
import PropTypes from 'prop-types'
import { InitImagePage } from '../../components/deploy/InitImage'

class DeployDetail extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: null,
      id: window.location.pathname ? window.location.pathname.substr(window.location.pathname.lastIndexOf("/") + 1)
        : ""
    }
  }

  componentDidMount() {
    this.fetchDetail()
  }

  fetchDetail = () => {
    fetchAndNotification({
      url: `cluster/${this.state.id}/`,
      method: 'get',
      notifications:{
        error: `获取数据失败！`,
      }
    }).then((result) => {
      this.setState({
        spinning: false,
        data: result.data
      })
    })
  }

  refresh = () => {
    this.props.dispatch({ type: 'deploy/refresh' })
  };

  render() {
      const Detail = ({data}) => {
      const content = []
      for (let key in data) {
          if ( key != 'key' & key != 'id' & key != 'name' ){
          content.push(
            <pre style={{'overflow-y':'scroll','max-height':'700px'}}>
            <div key={key} className={styles.item}>
            <div>{key}</div>
            <div>{String(data[key])}</div>
            </div>
            </pre>)
          }
      }
      //console.log('content: ', content)
      return (<div className="content-inner">
        <div className={styles.content}>
          {content}
        </div>
      </div>)
    }
    return (
      <Spin spinning={this.state.spinning}>
        <div className="action-btn-container">
          <InitImagePage {...this.modalProps}/>
        </div>
            <h1>{this.state.data ? this.state.data.name :null}</h1>
            <Detail data={this.state.data}/>
      </Spin>
    )
  }
}


function mapStateToProps ({ deploy }) {
  return {
    host:deploy,
  }
}

DeployDetail.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object,
}

export default connect(mapStateToProps)(DeployDetail)
