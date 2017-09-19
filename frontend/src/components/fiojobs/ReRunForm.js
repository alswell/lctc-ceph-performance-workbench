/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal, Row, Col, Select, Checkbox } from 'antd'
const { TextArea } = Input;
import { Link } from 'dva/router'
import PropTypes from 'prop-types'
import './TestForm.less'
import { fetchAndNotification } from '../../services/restfulService'
const FormItem = Form.Item

function hasErrors (fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field])
}

class TestTestForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: {},
      clusters: {},
      clients: [],
      pools: [],
      imagecount: 0,
      images: [],
      setvaluejobname: false,
      setvaluebs: false,
      setvaluepoolname: false,
      setvalueiodepth: false,
      setvaluenumjob: false,
      setvaluerwmixread: false,
      setvaluecluster: false,
      setvalueimagename: false,
      setvalueimagecount: false,
      setvaluefiotype: false,
      setvalueruntime: false,
      setvaluefiopara: false,
      setvaluecephconfig: false,
      setvaluesysdata: false,
      setvalueclient: false,
    }
  }

  componentDidMount () {
    // To disabled submit button at the beginning.
    this.props.form.validateFields()
    this.fetchDetail()
    this.fetchCluster()
  }

  fetchDetail = () => {
    fetchAndNotification({
      //url: `sarcpu?caseid=${this.state.id}`,
      url: `jobdetail?jobid=${this.props.record.id}`,
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

  fetchCluster = () => {
    fetchAndNotification({
      url: `cluster`,
      method: 'get',
      notifications:{
        error: `获取数据失败！`,
      }
    }).then((result) => {
      this.setState({
        spinning: false,
        clusters: result.data.data
      })
    })
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values)

        this.props.onCancel()
        fetchAndNotification({
          url: 'create',
          method: 'post',
          params: values,
          notifications: {
            title: 'create Action',
            success: `创建${values.jobname} 操作成功！`,
            error: `创建${values.jobname} 操作失败！`,
          },
        }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.props.refresh()
        })
      }
    })
  };

  handleImagecountChange = (value) => {
    this.props.form.setFieldsValue({
      imagename: '',
    });
    const clustervalue = this.props.form.getFieldValue('cluster');
    for (let i=0; i<this.state.clusters.length; i++) {
      if (this.state.clusters[i].clustername == clustervalue ) {
        fetchAndNotification({
            url: `images/${this.state.clusters[i].id}/`,
            method: 'get',
            params: { imagecount: imagecountvalue },
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              images: result.data
            })
          })
      }
    }
  }

  handleChange = (value) => {
    //console.log(`selected ${value}`);
    for (let i=0; i<this.state.clusters.length; i++) {
      if (this.state.clusters[i].clustername == value) {
        fetchAndNotification({
          url: `clients?id=${this.state.clusters[i].id}`,
          method: 'get',
          notifications:{
            error: `获取数据失败！`,
          }
        }).then((result) => {
          this.setState({
            clients: result.data
           })
        })
        fetchAndNotification({
          url: `pools/${this.state.clusters[i].id}/`,
          method: 'get',
          notifications:{
            error: `获取数据失败！`,
          }
        }).then((result) => {
          this.setState({
            pools: result.data
          })
        })
        const imagecountvalue = this.props.form.getFieldValue('imagecount');
        fetchAndNotification({
            url: `images/${this.state.clusters[i].id}/`,
            method: 'get',
            params: { imagecount: imagecountvalue },
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              images: result.data
            })
          })
      }
    }
    this.props.form.setFieldsValue({
      imagename: '',
      poolname: 'rbd',
      client: [],
    });
  };


  render () {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched, getFieldValue, setFieldsValue } = this.props.form
    
    // Only show error after a field is touched.
    const userNameError = isFieldTouched('userName') && getFieldError('userName')
    const passwordError = isFieldTouched('password') && getFieldError('password')
    const emailError = isFieldTouched('email') && getFieldError('email')
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 6 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 14 },
      },
    };
    const formItemLayoutWithOutLabel = {
      wrapperCol: {
        xs: { span: 24, offset: 0 },
        sm: { span: 11, offset: 6 },
      },
    };

    let gotoinitimage = []
    const clustervalue = getFieldValue('cluster')
    for (let i=0; i<this.state.clusters.length; i++) {
      if  (this.state.clusters[i].clustername == clustervalue) {
        gotoinitimage.push(<Link to={`cluster/${this.state.clusters[i].id}`}>Create image</Link>)
      }
    }
    const getcluster = [];
    if ( this.state.clusters.length > 0 ) {
      for (let i=0; i<this.state.clusters.length; i++) {
        getcluster.push(<Option key={this.state.clusters[i].clustername}>{this.state.clusters[i].clustername}</Option>)
      }
    }
    else{
      getcluster.push(<Option key={1}></Option>)
    }

    const rwmixread = [];
    for (let i = 0; i <= 100; i=i+10) {
      rwmixread.push(<Option key={i}>{i}</Option>);
    }

    let getclients = [];
    if ( this.state.clients.length > 0 ) {
      for (let i=0; i<this.state.clients.length; i++) {
        getclients.push(<Option key={this.state.clients[i]}>{this.state.clients[i]}</Option>)
      }
    }
    else{
      getclients.push(<Option key={1}></Option>)
    }
    
    let getpools = [];
    if ( this.state.pools.length > 0 ) {
      for (let i=0; i<this.state.pools.length; i++) {
        getpools.push(<Option key={this.state.pools[i]}>{this.state.pools[i]}</Option>)
      }
    }
    else{
      getpools.push(<Option key={1}></Option>)
    }

    let getimages = [];
    if ( this.state.images.length > 0 ) {
      for (let i=0; i<this.state.images.length; i++) {
        getimages.push(<Option key={this.state.images[i]}>{this.state.images[i]}</Option>)
      }
    }
    else{
      getimages.push(<Option key={1}></Option>)
    }

    const testset = () => {
      const bsvalue = getFieldValue('bs');
      if ( bsvalue != this.props.data.blocksize ){
        setFieldsValue({
          bs: this.props.data.blocksize,
        });
      }
    }

    let jobnamevalue = getFieldValue('jobname');
    if (this.props.visible && this.state.data != {} && this.state.setvaluejobname == false && jobnamevalue != this.state.data.jobname ){
      setFieldsValue({
        jobname: this.state.data.jobname,
      });
      this.setState({
        setvaluejobname: true,
      })
    }
    if ( this.state.clients.length == 0 || this.state.pools.length == 0 ){
      for (let i=0; i<this.state.clusters.length; i++) {
        if (this.state.clusters[i].clustername == clustervalue ) {
          fetchAndNotification({
            url: `clients?id=${this.state.clusters[i].id}`,
            method: 'get',
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              clients: result.data
            })
          })
          fetchAndNotification({
            url: `pools/${this.state.clusters[i].id}/`,
            method: 'get',
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              pools: result.data
            })
          })
        }
      }
    }
    if ( this.props.visible && this.state.data != {} && clustervalue != this.state.data.cluster && this.state.setvaluecluster == false ){
      setFieldsValue({
        cluster: this.state.data.cluster,
      });
      this.setState({
        setvaluecluster: true,
      })
    }
    const bsvalue = getFieldValue('bs');
    if ( this.props.visible && this.state.data != {} && bsvalue != this.state.data.bs && this.state.setvaluebs == false){
      setFieldsValue({
        bs: this.state.data.bs,
      });
      this.setState({
        setvaluebs: true,
      })
    }
    const fiotypevalue = getFieldValue('fiotype');
    if ( this.props.visible && this.state.data != {} && fiotypevalue != this.state.data.fiotype && this.state.setvaluefiotype == false ){
      setFieldsValue({
        fiotype: this.state.data.fiotype,
      });
      this.setState({
        setvaluefiotype: true,
      })
    }
    const rwmixreadvalue = getFieldValue('rwmixread');
    if ( this.props.visible && this.state.data != {} && rwmixreadvalue != this.state.data.rwmixread && this.state.setvaluerwmixread == false ){
      setFieldsValue({
        rwmixread: this.state.data.rwmixread,
      });
      this.setState({
        setvaluerwmixread: true,
      })
    }
    const iodepthvalue = getFieldValue('iodepth');
    if ( this.props.visible && this.state.data != {} && iodepthvalue != this.state.data.iodepth && this.state.setvalueiodepth == false ){
      setFieldsValue({
        iodepth: this.state.data.iodepth,
      });
      this.setState({
        setvalueiodepth: true,
      })
    }
    const numjobvalue = getFieldValue('numjob');
    if ( this.props.visible && this.state.data != {} && numjobvalue != this.state.data.numjob && this.state.setvaluenumjob == false ){
      setFieldsValue({
        numjob: this.state.data.numjob,
      });
      this.setState({
        setvaluenumjob: true,
      })
    }
    const imagenamevalue = getFieldValue('imagename');
    if ( this.props.visible && this.state.data != {} && imagenamevalue != this.state.data.imagename && this.state.setvalueimagename == false ){
      setFieldsValue({
        imagename: this.state.data.imagename,
      });
      this.setState({
        setvalueimagename: true,
      })
    }
    const poolnamevalue = getFieldValue('poolname');
    if ( this.props.visible && this.state.data != {} && poolnamevalue != this.state.data.poolname && this.state.setvaluepoolname == false ){
      setFieldsValue({
        poolname: this.state.data.poolname,
      });
      this.setState({
        setvaluepoolname: true,
      })
    }
    const runtimevalue = getFieldValue('runtime');
    if ( this.props.visible && this.state.data != {} && runtimevalue != this.state.data.runtime && this.state.setvalueruntime == false ){
      setFieldsValue({
        runtime: this.state.data.runtime,
      });
      this.setState({
        setvalueruntime: true,
      })
    }
    const imagecountvalue = getFieldValue('imagecount');
    if ( this.props.visible && this.state.imagecount != imagecountvalue && imagecountvalue != undefined ) {
      this.setState({
          imagecount: imagecountvalue
      })
      for (let i=0; i<this.state.clusters.length; i++) {
        if (this.state.clusters[i].clustername == clustervalue ) {
          fetchAndNotification({
            url: `images/${this.state.clusters[i].id}/`,
            method: 'get',
            params: { imagecount: imagecountvalue },
            notifications:{
              error: `获取数据失败！`,
            }
          }).then((result) => {
            this.setState({
              images: result.data
            })
          })
        }
      }
    }
    if ( this.props.visible && this.state.data != {} && imagecountvalue != this.state.data.imagecount && this.state.setvalueimagecount == false ){
      setFieldsValue({
        imagecount: this.state.data.imagecount,
      });
      this.setState({
        setvalueimagecount: true,
      })
    }
    const fioparavalue = getFieldValue('fiopara');
    if ( this.props.visible && this.state.data != {} && fioparavalue != this.state.data.fiopara && this.state.setvaluefiopara == false ){
      setFieldsValue({
        fiopara: this.state.data.fiopara,
      });
      this.setState({
        setvaluefiopara: true,
      })
    }
    const cephconfigvalue = getFieldValue('cephconfig');
    if ( this.props.visible && this.state.data != {} && cephconfigvalue != this.state.data.cephconfig && this.state.setvaluecephconfig == false ){
      setFieldsValue({
        cephconfig: this.state.data.cephconfig,
      });
      this.setState({
        setvaluecephconfig: true,
      })
    }
    const sysdatavalue = getFieldValue('sysdata');
    if ( this.props.visible && this.state.data != {} && sysdatavalue != this.state.data.sysdata && this.state.setvaluesysdata == false ){
      setFieldsValue({
        sysdata: this.state.data.sysdata,
      });
      this.setState({
        setvaluesysdata: true,
      })
    }
    const clientvalue = getFieldValue('client');
    if ( this.props.visible && this.state.data != {} && clientvalue != this.state.data.clients && this.state.setvalueclient == false ){
      //console.log(this.state.data.clients)
      setFieldsValue({
        client: this.state.data.clients,
      });
      this.setState({
        setvalueclient: true,
      })
    }

    return (
      <Modal
        visible={this.props.visible}
        title="Create a new job"
        okText="Create"
        footer={null}
        onCancel={this.props.onCancel}
        width={800}
        // onOk={this.onCreate}
      >
        <Form onSubmit={this.handleSubmit}>
          <FormItem
            {...formItemLayout}
            label="JobName"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('jobname', {
              rules: [
                { required: true, message: 'Please input the jobname!' },
              ],
            })(
              <Input placeholder="Jobname" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Cluster"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('cluster', {
              rules: [
                { required: true, message: 'Please select read write type!' },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
                onChange={this.handleChange}
              >
                {getcluster}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Ceph Client"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('client', {
              rules: [{ required: true, message: 'Please select the client!' }],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                 {getclients}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Fio Type"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('fiotype', {
              rules: [
                { required: true, message: 'Please select read write type!' },
              ],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                <Option key="rw">rw</Option>
                <Option key="randrw">randrw</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="RW MixRead(%)"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('rwmixread', {
              rules: [
                { required: true, message: 'Please select the RW MixRead!' },
              ],
              })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                {rwmixread}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Block Size"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('bs', {
              rules: [
                { required: true, message: 'Please select Block Size!' },
              ],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                <Option key="4k">4k</Option>
                <Option key="8k">8k</Option>
                <Option key="16k">16k</Option>
                <Option key="32k">32k</Option>
                <Option key="64k">64k</Option>
                <Option key="128k">128k</Option>
                <Option key="256k">256k</Option>
                <Option key="512k">512k</Option>
                <Option key="1024k">1024k</Option>
                <Option key="2048k">2048k</Option>
                <Option key="4M">4M</Option>
                <Option key="8M">8M</Option>
                <Option key="16M">16M</Option>
                <Option key="32M">32M</Option>
                <Option key="64M">64M</Option>
                <Option key="128M">128M</Option>
              </Select>
            )}
            {testset}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="IODepth"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('iodepth', {
              rules: [
                { required: true, message: 'Please select IODepth!' },
              ],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                <Option key="1">1</Option>
                <Option key="4">4</Option>
                <Option key="8">8</Option>
                <Option key="16">16</Option>
                <Option key="32">32</Option>
                <Option key="64">64</Option>
                <Option key="128">128</Option>
                <Option key="256">256</Option>
                <Option key="512">512</Option>
                <Option key="1024">1024</Option>
              </Select>
            )}
          </FormItem>
           <FormItem
            {...formItemLayout}
            label="Num Job"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('numjob', {
              rules: [
                { required: true, message: 'Please select Num Job!' },
              ],
            })(
              <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                <Option key="1">1</Option>
                <Option key="4">4</Option>
                <Option key="8">8</Option>
                <Option key="16">16</Option>
                <Option key="32">32</Option>
                <Option key="64">64</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Runtime(s)"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('runtime', {
              rules: [
                { required: true, message: 'Please input the Run Time!' },
              ],
            })(
              <Input placeholder="120" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Pool"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('poolname', {
              rules: [
                { required: true, message: 'Please input the Pool Name!' },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                {getpools}
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Image Count"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('imagecount', {
              rules: [
                { required: true, message: 'Please input the Image Count!' },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
                onChange={this.handleImagecountChange}
              >
                <Option key="1">1</Option>
                <Option key="2">2</Option>
                <Option key="3">3</Option>
                <Option key="4">4</Option>
                <Option key="5">5</Option>
                <Option key="6">6</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Image Name"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('imagename', {
              rules: [
                { required: true, message: 'Please input the Image Name!' },
              ],
            })(
              <Select
                style={{ width: '100%' }}
                placeholder="Please select"
              >
                {getimages}
              </Select>
            )}
            {gotoinitimage}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Ceph config"
            help={userNameError || ''}
          >
            {getFieldDecorator(`cephconfig`, {
              validateTrigger: ['onChange', 'onBlur'],
              rules: [{
                required: false,
                whitespace: true,
                message: "Please input ceph config.",
              }],
              })(
              <TextArea placeholder="debug_paxos=35" style={{ width: '100%', marginRight: 8, height: 100 }} />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="fio parameter"
            help={userNameError || ''}
          >
            {getFieldDecorator(`fiopara`, {
              validateTrigger: ['onChange', 'onBlur'],
              rules: [{
                required: false,
                whitespace: true,
                message: "Please input fio parameter.",
              }],
              })(
              <TextArea placeholder="rw=rw" style={{ width: '100%', marginRight: 8, height: 100 }} />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="sysdata collect"
          >
            {getFieldDecorator(`sysdata`, {
              rules: [{
                required: false,
              }],
              })(
              <Checkbox.Group>
                <Row>
                  <Col span={3}><Checkbox value="sar">sar</Checkbox></Col>
                  <Col span={4}><Checkbox value="iostat">iostat</Checkbox></Col>
                  <Col span={6}><Checkbox value="cephstatus">ceph status</Checkbox></Col>
                  <Col span={6}><Checkbox value="perfdump">perf dump</Checkbox></Col>
                  <Col span={8}><Checkbox value="lsblk">lsblk&smartctl</Checkbox></Col>
                </Row>
              </Checkbox.Group>
            )}
          </FormItem>
          <FormItem>
            <Button
              type="primary"
              htmlType="submit"
              disabled={hasErrors(getFieldsError())}
            >
              Create
            </Button>
          </FormItem>
        </Form>
      </Modal>
    )
  }
}

TestTestForm.propTypes = {
  form: PropTypes.object,
  onCancel: PropTypes.function,
  visible: PropTypes.boolean,
  record: PropTypes.array,
  data: PropTypes.array,
}

const TestForm = Form.create()(TestTestForm)

export default TestForm
