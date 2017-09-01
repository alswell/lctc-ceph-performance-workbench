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
import FioJobsModal from '../../components/modals/FioJobsModal'
import { fetchAndNotification } from '../../services/restfulService'
import { CollectionsPage } from '../../components/fiojobs/CreateModal'

const confirm = Modal.confirm

class HostPage extends React.Component {
  // constructor (props) {
  //   super(props)
  // }

  componentDidMount () {

  }

  handleMenuClick = (record, e) => {
    if (e.key === '1') {
      confirm({
        title: 'Are you sure Cancel this Job?',
        onOk :()=> {
          console.log(record)
          fetchAndNotification({
            url: 'fiojobs',
            method: 'put',
            params: { id: record.id, status: "Canceling" },
            notifications: {
              title: 'Cancel Action',
              success: `${record.name} 操作成功！`,
              error: `${record.name} 操作失败！`,
            },
          }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.refresh()
        })
        },
      })
    } else if (e.key === '2') {
      confirm({
        title: 'Are you sure delete this Job?',
        onOk :()=> {
          console.log(record)
          fetchAndNotification({
            url: 'fiojobs',
            method: 'delete',
            params: { id: record.id },
            notifications: {
              title: 'Delete Action',
              success: `${record.name} 操作成功！`,
              error: `${record.name} 操作失败！`,
            },
          }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.refresh()
        })
        },
      })
    }
  };

  showModal = (key) => {
    let { dispatch } = this.props
    dispatch({
      type: 'fiojobs/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'fiojobs/refresh' })
  };

  init = () => {
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
          title: 'Job Name',
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
        {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Cancel' }, { key: '2', name: 'Delete' }]}
            />)
          },
        }
      ],
      fetchData: {
        url: `fiojobs`,
        params: null,
      },
      errorMsg: 'get job table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "fiojobs/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.iopsModalProps = {
      visible: this.props.host.iopsModalVisible,
      maskClosable: true,
      title: 'IOPS Chart',
      type: 'iops',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'fiojobs/hideModal',
          payload: {
            key: 'iopsModalVisible',
          },
        })
      },
    }
    this.latModalProps = {
      visible: this.props.host.latModalVisible,
      maskClosable: true,
      title: 'LAT Chart',
      type: 'lat',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'fiojobs/hideModal',
          payload: {
            key: 'latModalVisible',
          },
        })
      },
    }
    this.bwModalProps = {
      visible: this.props.host.bwModalVisible,
      maskClosable: true,
      title: 'BW Chart',
      type: 'bw',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'fiojobs/hideModal',
          payload: {
            key: 'bwModalVisible',
          },
        })
      },
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
                <Button type="primary" onClick={this.showModal.bind(this, 'iopsModalVisible')}
                  disabled={this.props.host.selectedItems.length === 0}
                >IOPS Chart</Button>
                <Button type="primary" onClick={this.showModal.bind(this, 'latModalVisible')}
                  disabled={this.props.host.selectedItems.length === 0}
                >Lat Chart</Button>
                <Button type="primary" onClick={this.showModal.bind(this, 'bwModalVisible')}
                  disabled={this.props.host.selectedItems.length === 0}
                >BW Chart</Button>
              </div>
              <DataTable
                {...this.tableDataProps}
              />
            </Card>
          </Col>
        </Row>
        {this.props.host.iopsModalVisible && <FioJobsModal {...this.iopsModalProps} />}
        {this.props.host.latModalVisible && <FioJobsModal {...this.latModalProps} />}
        {this.props.host.bwModalVisible && <FioJobsModal {...this.bwModalProps} />}
      </div>
    )
  }
}


function mapStateToProps ({ fiojobs }) {
  return {
    host:fiojobs,
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

