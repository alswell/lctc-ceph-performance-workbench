/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal, Row, Col } from 'antd'
const { TextArea } = Input;
import PropTypes from 'prop-types'
import './TestForm.less'
import { fetchAndNotification } from '../../services/restfulService'
const FormItem = Form.Item

function hasErrors (fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field])
}

let bsid = 1;
let iodepthid = 1;
let clientid = 1;
let fiotypeid = 1;
let numjobid = 1;
let cephconfigid = 0;
let fioparaid = 0;
class TestTestForm extends React.Component {

  componentDidMount () {
    // To disabled submit button at the beginning.
    this.props.form.validateFields()
  }

  bsremove = (k) => {
    const { form } = this.props;

    const bskeys = form.getFieldValue('bskeys');

    if (bskeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      bskeys: bskeys.filter(key => key !== k),
    });
  }

  bsadd = () => {
    bsid++;
    const { form } = this.props;

    const bskeys = form.getFieldValue('bskeys');
    const nextbsKeys = bskeys.concat(bsid);

    form.setFieldsValue({
      bskeys: nextbsKeys,
    });
  }

  iodepthremove = (k) => {
    const { form } = this.props;

    const iodepthkeys = form.getFieldValue('iodepthkeys');

    if (iodepthkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      iodepthkeys: iodepthkeys.filter(key => key !== k),
    });
  }

  iodepthadd = () => {
    iodepthid++;
    const { form } = this.props;

    const iodepthkeys = form.getFieldValue('iodepthkeys');
    const nextiodepthKeys = iodepthkeys.concat(iodepthid);

    form.setFieldsValue({
      iodepthkeys: nextiodepthKeys,
    });
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

  fiotyperemove = (k) => {
    const { form } = this.props;

    const fiotypekeys = form.getFieldValue('fiotypekeys');

    if (fiotypekeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      fiotypekeys: fiotypekeys.filter(key => key !== k),
    });
  }

  fiotypeadd = () => {
    fiotypeid++;
    const { form } = this.props;

    const fiotypekeys = form.getFieldValue('fiotypekeys');
    const nextfiotypeKeys = fiotypekeys.concat(fiotypeid);

    form.setFieldsValue({
      fiotypekeys: nextfiotypeKeys,
    });
  }

  numjobremove = (k) => {
    const { form } = this.props;

    const numjobkeys = form.getFieldValue('numjobkeys');

    if (numjobkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      numjobkeys: numjobkeys.filter(key => key !== k),
    });
  }

  numjobadd = () => {
    numjobid++;
    const { form } = this.props;

    const numjobkeys = form.getFieldValue('numjobkeys');
    const nextnumjobKeys = numjobkeys.concat(numjobid);

    form.setFieldsValue({
      numjobkeys: nextnumjobKeys,
    });
  }

  cephconfigremove = (k) => {
    const { form } = this.props;

    const cephconfigkeys = form.getFieldValue('cephconfigkeys');

    if (cephconfigkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      cephconfigkeys: cephconfigkeys.filter(key => key !== k),
    });
  }

  cephconfigadd = () => {
    cephconfigid++;
    const { form } = this.props;

    const cephconfigkeys = form.getFieldValue('cephconfigkeys');
    const nextcephconfigKeys = cephconfigkeys.concat(cephconfigid);

    form.setFieldsValue({
      cephconfigkeys: nextcephconfigKeys,
    });
  }

  fiopararemove = (k) => {
    const { form } = this.props;

    const fioparakeys = form.getFieldValue('fioparakeys');

    if (fioparakeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      fioparakeys: fioparakeys.filter(key => key !== k),
    });
  }

  fioparaadd = () => {
    fioparaid++;
    const { form } = this.props;

    const fioparakeys = form.getFieldValue('fioparakeys');
    const nextfioparaKeys = fioparakeys.concat(fioparaid);

    form.setFieldsValue({
      fioparakeys: nextfioparaKeys,
    });
  }

  rwmixreadremove = (k) => {
    const { form } = this.props;

    const rwmixreadkeys = form.getFieldValue('rwmixreadkeys');

    if (rwmixreadkeys.length === 0) {
      return;
    }


    form.setFieldsValue({
      rwmixreadkeys: rwmixreadkeys.filter(key => key !== k),
    });
  }

  rwmixreadadd = () => {
    rwmixreadid++;
    const { form } = this.props;

    const rwmixreadkeys = form.getFieldValue('rwmixreadkeys');
    const nextrwmixreadKeys = rwmixreadkeys.concat(rwmixreadid);

    form.setFieldsValue({
      rwmixreadkeys: nextrwmixreadKeys,
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
        })
      }
    })
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

    getFieldDecorator('bskeys', { initialValue: [] });
    const bskeys = getFieldValue('bskeys');
    const bsformItems = bskeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayoutWithOutLabel}
          required={false}
          bskey={k}
        >
          {getFieldDecorator(`bs-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input block size or delete this field.",
            }],
          })(
            <Input placeholder="4k" style={{ width: '60%', marginRight: 8 }} />
          )}
          {bskeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={bskeys.length === 0}
              onClick={() => this.bsremove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

    getFieldDecorator('iodepthkeys', { initialValue: [] });
    const iodepthkeys = getFieldValue('iodepthkeys');
    const iodepthformItems = iodepthkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayoutWithOutLabel}
          required={false}
          iodepthkeys={k}
        >
          {getFieldDecorator(`iodepth-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input iodepth or delete this field.",
            }],
          })(
            <Input placeholder="1" style={{ width: '60%', marginRight: 8 }} />
          )}
          {iodepthkeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={iodepthkeys.length === 0}
              onClick={() => this.iodepthremove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

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
            <Input placeholder="10.240.217.101" style={{ width: '60%', marginRight: 8 }} />
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

    getFieldDecorator('fiotypekeys', { initialValue: [] });
    const fiotypekeys = getFieldValue('fiotypekeys');
    const fiotypeformItems = fiotypekeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayoutWithOutLabel}
          required={false}
          fiotypekey={k}
        >
          {getFieldDecorator(`fiotype-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input block size or delete this field.",
            }],
          })(
            <Input placeholder="rw|randrw" style={{ width: '60%', marginRight: 8 }} />
          )}
          {fiotypekeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={fiotypekeys.length === 0}
              onClick={() => this.fiotyperemove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

    getFieldDecorator('rwmixreadkeys', { initialValue: [] });
    const rwmixreadkeys = getFieldValue('rwmixreadkeys');
    const rwmixreadformItems = rwmixreadkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayoutWithOutLabel}
          required={false}
          rwmixreadkey={k}
        >
          {getFieldDecorator(`rwmixread-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input block size or delete this field.",
            }],
          })(
            <Input placeholder="100" style={{ width: '60%', marginRight: 8 }} />
          )}
          {rwmixreadkeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={rwmixreadkeys.length === 0}
              onClick={() => this.rwmixreadremove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

    getFieldDecorator('numjobkeys', { initialValue: [] });
    const numjobkeys = getFieldValue('numjobkeys');
    const numjobformItems = numjobkeys.map((k, index) => {
      return (
        <FormItem
          {...formItemLayoutWithOutLabel}
          required={false}
          numjobkey={k}
        >
          {getFieldDecorator(`numjob-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input Num Job or delete this field.",
            }],
          })(
            <Input placeholder="1" style={{ width: '60%', marginRight: 8 }} />
          )}
          {numjobkeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={numjobkeys.length === 0}
              onClick={() => this.numjobremove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

    getFieldDecorator('cephconfigkeys', { initialValue: [] });
    const cephconfigkeys = getFieldValue('cephconfigkeys');
    const cephconfigformItems = cephconfigkeys.map((k, index) => {
      return (
        <FormItem
          {...(index === 0 ? formItemLayout : formItemLayoutWithOutLabel)}
          label={index === 0 ? 'Ceph config' : ''}
          required={false}
          cephconfigkey={k}
        >
          {getFieldDecorator(`cephconfig-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input block size or delete this field.",
            }],
          })(
            <TextArea placeholder="debug_paxos=35" style={{ width: '60%', marginRight: 8 }} />
          )}
          {cephconfigkeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={cephconfigkeys.length === 0}
              onClick={() => this.cephconfigremove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

    getFieldDecorator('fioparakeys', { initialValue: [] });
    const fioparakeys = getFieldValue('fioparakeys');
    const fioparaformItems = fioparakeys.map((k, index) => {
      return (
        <FormItem
          {...(index === 0 ? formItemLayout : formItemLayoutWithOutLabel)}
          label={index === 0 ? 'fio parameter' : ''}
          required={false}
          fioparakey={k}
        >
          {getFieldDecorator(`fiopara-${k}`, {
            validateTrigger: ['onChange', 'onBlur'],
            rules: [{
              required: true,
              whitespace: true,
              message: "Please input fio parameter or delete this field.",
            }],
          })(
            <Input placeholder="rw=rw" style={{ width: '60%', marginRight: 8 }} />
          )}
          {fioparakeys.length > 0 ? (
            <Icon
              className="dynamic-delete-button"
              type="minus-circle-o"
              disabled={fioparakeys.length === 0}
              onClick={() => this.fiopararemove(k)}
            />
          ) : null}
        </FormItem>
      );
    });

    return (
      <Modal
        visible={this.props.visible}
        title="Create a new job"
        okText="Create"
        footer={null}
        onCancel={this.props.onCancel}
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
            label="Ceph Client"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            <Row gutter={8}>
              <Col span={12}>
                {getFieldDecorator('client-1', {
                  rules: [{ required: true, message: 'Please input the client!' }],
                })(
                  <Input size="large" placeholder="10.240.217.101"/>
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
            <Row gutter={8}>
              <Col span={12}>
                {getFieldDecorator('fiotype-1', {
                  rules: [{ required: true, message: 'Please input the FIO type!' }],
                })(
                  <Input size="large" placeholder="rw|randrw"/>
                )}
              </Col>
              <Col span={12}>
                <Button type="dashed" onClick={this.fiotypeadd} style={{ width: '100%' }}>
                  <Icon type="plus" /> Add fio Type
                </Button>
              </Col>
            </Row>
          </FormItem> 
          {fiotypeformItems}
          <FormItem
            {...formItemLayout}
            label="RW MixRead(%)"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            <Row gutter={8}>
              <Col span={12}>
                {getFieldDecorator('rwmixread-1', {
                  rules: [
                    { required: true, message: 'Please input the RW MixRead!' },
                  ],
                })(
                  <Input placeholder="100" />
                )}
              </Col>
              <Col span={12}>
                <Button type="dashed" onClick={this.rwmixreadadd} style={{ width: '100%' }}>
                  <Icon type="plus" /> Add RW MixRead
                </Button>
              </Col>
            </Row>
         </FormItem>
          <FormItem
            {...formItemLayout}
            label="Block Size"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            <Row gutter={8}>
              <Col span={12}>
                {getFieldDecorator('bs-1', {
                  rules: [{ required: true, message: 'Please input the Block Size!' }],
                })(
                  <Input size="large" placeholder="4k"/>
                )}
              </Col>
              <Col span={12}>
            <Button type="dashed" onClick={this.bsadd} style={{ width: '100%' }}>
              <Icon type="plus" /> Add Block Size
            </Button>
              </Col>
            </Row>
          </FormItem>
          {bsformItems}
          <FormItem
            {...formItemLayout}
            label="IODepth"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            <Row gutter={8}>
              <Col span={12}>
                {getFieldDecorator('iodepth-1', {
                  rules: [{ required: true, message: 'Please input the IODepth!' }],
                })(
                  <Input size="large" placeholder="1"/>
                )}
              </Col>
              <Col span={12}>
                <Button type="dashed" onClick={this.iodepthadd} style={{ width: '100%' }}>
                  <Icon type="plus" /> Add IODepth
                </Button>
              </Col>
            </Row>
          </FormItem>
          {iodepthformItems}
          <FormItem
            {...formItemLayout}
            label="Num Job"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            <Row gutter={8}>
              <Col span={12}>
                {getFieldDecorator('numjob-1', {
                  rules: [{ required: true, message: 'Please input the Num Job!' }],
                })(
                  <Input size="large" placeholder="1"/>
                )}
              </Col>
              <Col span={12}>
            <Button type="dashed" onClick={this.numjobadd} style={{ width: '100%' }}>
              <Icon type="plus" /> Add Num Job
            </Button>
              </Col>
            </Row>
          </FormItem>
          {numjobformItems}
          <FormItem
            {...formItemLayout}
            label="Runtime(s)"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('Runtime', {
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
            {getFieldDecorator('PoolName', {
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
            {getFieldDecorator('Image Count', {
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
            {getFieldDecorator('Image Name', {
              rules: [
                { required: true, message: 'Please input the Image Name!' },
              ],
            })(
              <Input placeholder="testimage_102400" />
            )}
          </FormItem>
          {cephconfigformItems}
          <FormItem {...formItemLayoutWithOutLabel}>
            <Button type="dashed" onClick={this.cephconfigadd} style={{ width: '100%' }}>
              <Icon type="plus" /> Add modify Ceph Config
            </Button>
          </FormItem>
          {fioparaformItems}
          <FormItem {...formItemLayoutWithOutLabel}>
            <Button type="dashed" onClick={this.fioparaadd} style={{ width: '100%' }}>
              <Icon type="plus" /> Add more fio paramaters
            </Button>
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
