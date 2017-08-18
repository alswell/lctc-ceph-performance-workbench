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
import BatchModal from '../../components/modals/BatchModal'
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
      let { dispatch } = this.props
      dispatch({
        type: 'host/showModal',
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
      type: 'host/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'fiojobs/refresh' })
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
          type: 'host/hideModal',
          payload: {
            key: 'modalVisible',
          },
        })
      },
    }

    this.tableDataProps = {
      columns: [
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
          render: (text, record) => <Link to={`cephconfig?jobid=${record.id}`}>{text}</Link>,
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      fetchData: {
        url: `fiojobs`,
        params: null,
      },
      errorMsg: 'get job table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.batchModalProps = {
      visible: this.props.host.batchModalVisible,
      maskClosable: true,
      title: 'Batch Action Modal',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      fetchData: {
        url: 'host',
        method: 'delete',
      },
      onOk: (data) => {
        this.batchModalProps.onCancel()
        this.props.host.selectedItems.forEach((item) => {
          fetchAndNotification({
            url: 'host',
            method: 'delete',
            params: { ids: item.id },
            notifications: {
              title: 'batch Action',
              success: `${item.name} 操作成功！`,
              error: `${item.name} 操作失败！`,
            },
          })
        })
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'host/hideModal',
          payload: {
            key: 'batchModalVisible',
          },
        })
      },
    }

    this.createModalProps = {
      visible: this.props.host.createModalVisible,
      maskClosable: true,
      title: 'Batch Action Modal',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      fetchData: {
        url: 'host',
        method: 'delete',
      },
      onOk: (data) => {
        this.batchModalProps.onCancel()
        this.props.host.selectedItems.forEach((item) => {
          fetchAndNotification({
            url: 'host',
            method: 'delete',
            params: { ids: item.id },
            notifications: {
              title: 'batch Action',
              success: `${item.name} 操作成功！`,
              error: `${item.name} 操作失败！`,
            },
          })
        })
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'host/hideModal',
          payload: {
            key: 'createModalVisible',
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
            <Card title="远程数据">
              <div className="action-btn-container">
                <Button type="primary" onClick={this.refresh} icon="reload" />
                <Button type="primary" onClick={this.showModal.bind(this, 'batchModalVisible')}
                  disabled={this.props.host.selectedItems.length === 0}
                >Batch Action</Button>
                <CollectionsPage {...this.actionCollectionsProps}/>
              </div>
              <DataTable
                {...this.tableDataProps}
              />
            </Card>
          </Col>
        </Row>
        {this.props.host.modalVisible && <Modal {...this.modalProps} />}
        {this.props.host.batchModalVisible && <BatchModal {...this.batchModalProps} />}
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

