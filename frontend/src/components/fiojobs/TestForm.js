/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal, Row, Col, Select, Checkbox } from 'antd'
const { TextArea } = Input;
import PropTypes from 'prop-types'
import './TestForm.less'
import { fetchAndNotification } from '../../services/restfulService'
const FormItem = Form.Item

function hasErrors (fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field])
}

let clientid = 1;
class TestTestForm extends React.Component {
 constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      clusters: {},
      clients: [],
    }
  }

  componentDidMount () {
    // To disabled submit button at the beginning.
    this.props.form.validateFields()
    this.fetchCluster()
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

  clientremove = (k) => {
    const { form } = this.props;

    const clientkeys = form.getFieldValue('clientkeys');

    if (clientkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      clientkeys: clientkeys.filter(key => key !== k),
    });
  }

  clientadd = () => {
    clientid++;
    const { form } = this.props;

    const clientkeys = form.getFieldValue('clientkeys');
    const nextclientKeys = clientkeys.concat(clientid);

    form.setFieldsValue({
      clientkeys: nextclientKeys,
    });
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

  handleChange = (value) => {
      console.log(`selected ${value}`);
    };


  render () {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched, getFieldValue } = this.props.form

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

    getFieldDecorator('clientkeys', { initialValue: [] });
    const clientkeys = getFieldValue('clientkeys');
    const clientformItems = clientkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayoutWithOutLabel}
          required={false}
          clientkey={k}
        >
          {getFieldDecorator(`client-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input client or delete this field.",
            }],
          })(
            <Input placeholder="10.240.217.131" style={{ width: '60%', marginRight: 8 }} />
          )}
          {clientkeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={clientkeys.length === 0}
              onClick={() => this.clientremove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

    // getFieldDecorator('cluster', { initialValue: [] });
    // const clustername = getFieldValue('cluster');
    // console.log(clustername.length)
    // if (cluster.length > 0 ) {
        
    // }
    
    // const clientselectItems = this.state.clients.map((k, index) => {
    //   if ( node != undefined ) {
    //     //console.log('Node:',node)
    //     return (
    //       <Option key={node}>{node}</Option>
    //     );
    //   }
    //   else {
    //     return (
    //       <Option key={1}></Option>
    //     );
    //   }
    // });

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
                { required: true,},
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
            <Row gutter={8}>
              <Col span={12}>
                {getFieldDecorator('client-1', {
                  initialValue: "10.240.217.131",
                  rules: [{ required: true, message: 'Please input the client!' }],
                })(
                  <Input size="large" placeholder="10.240.217.131"/>
                )}
              </Col>
              <Col span={12}>
                <Button type="dashed" onClick={this.clientadd} style={{ width: '100%' }}>
                  <Icon type="plus" /> Add Client
                </Button>
              </Col>
            </Row>
          </FormItem>
           {clientformItems}
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
                onChange={this.handleChange}
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
                onChange={this.handleChange}
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
                onChange={this.handleChange}
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
              </Select>
            )}
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
                onChange={this.handleChange}
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
                onChange={this.handleChange}
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
              initialValue: "120",
              rules: [
                { required: true, message: 'Please input the Run Time!' },
              ],
            })(
              <Input placeholder="120" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Pool Name"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('poolname', {
              initialValue: "rbd",
              rules: [
                { required: true, message: 'Please input the Pool Name!' },
              ],
            })(
              <Input placeholder="rbd" />
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
              <Input placeholder="1" />
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
              <Input placeholder="testimage_102400" />
            )}
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
              initialValue: "perfdump",
              rules: [{
                required: false,
              }],
              })(
              <Checkbox.Group onChange={this.handleChange}>
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
}

const TestForm = Form.create()(TestTestForm)

export default TestForm
