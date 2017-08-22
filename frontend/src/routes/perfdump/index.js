/**
 * Created by chenkang1 on 2017/8/21.
 */

import React from "react";
import {connect} from 'dva';
import {Spin, Tabs} from 'antd';
import {fetchAndNotification} from "../../services/restfulService";
import styles from './index.less'

const TabPane = Tabs.TabPane;

class HostDetail extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: {},
      id: window.location.pathname ? window.location.pathname.substr(window.location.pathname.lastIndexOf("/") + 1)
        : ""
    }
  }

  componentDidMount() {
    this.fetchDetail()
  }

  fetchDetail = () => {
    fetchAndNotification({
      url: `perfdump/${this.state.id}/`,
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
    const Detail = ({cephConfig}) => {
      const content = []
      for (let key in cephConfig) {
          content.push(<div key={key} className={styles.item}>
            <div>{key}</div>
            <div>{String(cephConfig[key])}</div>
          </div>)
      }
      return (<div className="content-inner">
        <div className={styles.content}>
          {content}
        </div>
      </div>)
    }

    const OsdCard = ({perfdump}) => {
      const content = []
      for (let i=0; i<perfdump.length; i++) {
        content.push(
          <TabPane key={i} tab={perfdump[i].osd}>
            <Detail cephConfig={perfdump[i]}/>
          </TabPane>)
      }
      return (
        <Tabs type="card">
          {content}
        </Tabs>
      )
    }


    return (
      <Spin spinning={this.state.spinning}>
        <OsdCard perfdump={this.state.data}/>
      </Spin>
    )
  }
}


HostDetail.propTypes = {};


export default connect(host => host)(HostDetail);