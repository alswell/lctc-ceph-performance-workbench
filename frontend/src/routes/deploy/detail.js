/**
 * Created by chenkang1 on 2017/8/21.
 */

import React from "react";
import {connect} from 'dva';
import {Spin} from 'antd';
import {fetchAndNotification} from "../../services/restfulService";
import styles from './index.less'

class HostDetail extends React.Component {

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

  render() {
      const Detail = ({data}) => {
      const content = []
      for (let key in data) {
          if ( key != 'key' & key != 'id' & key != 'name' ){
          content.push(<div key={key} className={styles.item}>
            <div>{key}</div>
            <div>{String(data[key])}</div>
            </div>)
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
        <div className="content-inner">
          <h2>{this.state.data ? this.state.data.name :null}</h2>
          <Detail data={this.state.data}/>
        </div>
      </Spin>
    )
  }
}


HostDetail.propTypes = {};


export default connect(host => host)(HostDetail);
