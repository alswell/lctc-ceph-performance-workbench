/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'dva'
import DataTable from '../../components/BasicTable/DataTable'
import { Modal, Row, Col, Card, Button } from 'antd'
import { Link } from 'dva/router'
import DropOption from '../../components/DropOption/DropOption'
import { fetchAndNotification } from '../../services/restfulService'
import { CollectionsPage } from '../../components/deploy/CreateModal'

const confirm = Modal.confirm

class HostPage extends React.Component {
  // constructor (props) {
  //   super(props)
  // }

  componentDidMount () {

  }

  handleMenuClick = (record, e) => {
    if (e.key === '1') {
      let { dispatch } = this.props
      dispatch({
        type: 'deploy/showModal',
        payload: {
          key: 'modalVisible',
        },

      })
    } else if (e.key === '2') {
      confirm({
        title: 'Are you sure delete this record?',
        onOk () {
          console.log(record)
        },
      })
    }
  };

  showModal = (key) => {
    let { dispatch } = this.props
    dispatch({
      type: 'deploy/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'deploy/refresh' })
  };

  init = () => {
    this.modalProps = {
      visible: this.props.host.modalVisible,
      maskClosable: true,
      title: 'test',
      wrapClassName: 'vertical-center-modal',
      onOk: (data) => {
        console.log(data)
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'deploy/hideModal',
          payload: {
            key: 'modalVisible',
          },
        })
      },
    }

    this.tableDataProps = {
      columns: [
        {
          title: 'ID',
          dataIndex: 'id',
          key: 'id',
          width: 50,
          sorter: true,
        },
        {
          title: 'Cluster Name',
          dataIndex: 'name',
          key: 'name',
          // width: 64,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          // width: 100,
        }, {
          title: 'status',
          dataIndex: 'status',
          key: 'status',
          sorter: true,
          // width: 100,
         }, {
          title: 'test cases',
          dataIndex: 'casenum',
          key: 'casenum',
          render: (text, record) => <Link to={`fiotest?jobid=${record.id}`}>{text} test cases</Link>,
          // width: 100,
        }, {
          title: 'ceph config',
          dataIndex: 'ceph_config',
          key: 'ceph_config',
          render: (text, record) => <Link to={`cephconfig/${record.id}`}>{text}</Link>,
        }, 
        {
          title: 'sys info',
          //dataIndex: 'ceph_config',
          //key: 'ceph_config',
          render: (text, record) => <Link to={`sysinfo?jobid=${record.id}`}>sys info</Link>,
        },
      ],
      fetchData: {
        url: `cluster`,
        params: null,
      },
      errorMsg: 'get job table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "deploy/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }
  };

  actionCollectionsProps = {
    refresh:this.refresh
  };

  render () {
    this.init()

    return (
      <div className="content-inner">
        <Row gutter={32}>
          <Col lg={24} md={24}>
            <Card>
              <div className="action-btn-container">
                <CollectionsPage {...this.actionCollectionsProps}/>
              </div>
              <div className="action-btn-container">
                <Button type="primary" onClick={this.refresh} icon="reload" />
              </div>
              <DataTable
                {...this.tableDataProps}
              />
            </Card>
          </Col>
        </Row>
      </div>
    )
  }
}


function mapStateToProps ({ deploy }) {
  return {
    host:deploy,
  }
}

HostPage.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object,
}

export default connect(mapStateToProps)(HostPage)

