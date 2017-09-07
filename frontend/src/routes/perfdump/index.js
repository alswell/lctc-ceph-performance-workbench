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
    const OsdCard = ({perfdump}) => {
      const content = []
      for (let i=0; i<perfdump.length; i++) {
        content.push(
          <TabPane key={i} tab={perfdump[i].osd}>
            <pre style={{'overflow-y':'scroll','max-height':'700px'}}>
              {JSON.stringify(perfdump[i].data, null, 2) }
            </pre>
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