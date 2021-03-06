/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'dva'
import DataTable from '../../components/BasicTable/DataTable'
import { Modal, Row, Col, Card, Button, Icon, Input } from 'antd'
const { TextArea } = Input;
import { Link } from 'dva/router'
import DropOption from '../../components/DropOption/DropOption'
import FioJobsModal from '../../components/modals/FioJobsModal'
import { fetchAndNotification } from '../../services/restfulService'
import { CollectionsPage } from '../../components/fiojobs/CreateModal'
import { ReRunPage } from '../../components/fiojobs/ReRunModal'
import styles from './List.less'

const confirm = Modal.confirm

class EditableCell extends React.Component {
  state = {
    value: this.props.value,
    editable: false,
  }
  handleChange = (e) => {
    const value = e.target.value;
    this.setState({ value });
  }
  check = () => {
    this.setState({ editable: false });
    if (this.props.onChange) {
      this.props.onChange(this.state.value);
    }
  }
  edit = () => {
    this.setState({ editable: true });
  }
  render() {
    const { value, editable } = this.state;
    return (
      <div className={styles.editablecell}>
        {
          editable ?
            <div className={styles.editablecellinputwrapper}>
              <TextArea
                value={value}
                onChange={this.handleChange}
              />
              <Icon
                type="check"
                className={styles.editablecelliconcheck}
                onClick={this.check}
              />
            </div>
            :
            <div className={styles.editablecelltextwrapper}>
              <pre>
                {value || ' '}
              </pre>
              <Icon
                type="edit"
                className={styles.editablecellicon}
                onClick={this.edit}
              />
            </div>
        }
      </div>
    );
  }
}

class HostPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
    }
  }

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
    } else if (e.key === '3') {
      let { dispatch } = this.props
      dispatch({
        type: 'fiojobs/updateOperationItems',
        payload: {
          record,
        },
      })
    }
  };

  updateOperationItems = (record) => {
    let { dispatch } = this.props
    dispatch({
      type: 'fiojobs/updateOperationItems',
      payload: {
        record,
      },
    })
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

  onCellChange = (record, e) => {
    return (value) => {
      fetchAndNotification({
          url: 'fiojobs',
          method: 'put',
          params: { id: record.id, comments: value },
          notifications: {
            title: 'create Action',
            error: ` 操作失败！`,
          },
        })
    }
  }

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
          dataIndex: 'starttime',
          key: 'starttime',
          sorter: true,
          // width: 100,
        }, {
          title: 'status',
          dataIndex: 'status',
          key: 'status',
          sorter: true,
          width: 100,
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
          render: (text, record) => {
            return (
              <pre>
                <Link to={`cephconfig/${record.id}`}>{text}</Link>
              </pre>
            )
          },
        }, 
        {
          title: 'sys info',
          //dataIndex: 'ceph_config',
          //key: 'ceph_config',
          render: (text, record) => <Link to={`sysinfo?jobid=${record.id}`}>sys info</Link>,
        },
        {
          title: 'log link',
          //dataIndex: 'ceph_config',
          //key: 'ceph_config',
          render: (text, record) => <a href={`http://10.240.217.74/${record.jobdir}`}>log files</a>,
        },
        {
          title: 'comments',
          dataIndex: 'comments',
          key: 'comments',
          width: '150',
          render: (text, record) => (
            <EditableCell
            value={text}
            onChange={this.onCellChange(record)}
            />
          ),
        },
        {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption 
              onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[
                { key: '1', name: 'Cancel' },
                { key: '2', name: 'Delete' },
                { key: '3', name: 'Re-run' },
              ]}
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

    this.modalProps = {
      visible: this.props.host.modalVisible,
      maskClosable: true,
      title: 'test',
      wrapClassName: 'vertical-center-modal',
      record: this.props.host.record,
      data: this.state.data,
      refresh:this.refresh,
      onOk: (data) => {
        console.log(data)
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'fiojobs/hideModal',
          payload: {
            key: 'modalVisible',
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
        {this.props.host.modalVisible && <ReRunPage {...this.modalProps} />}
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

