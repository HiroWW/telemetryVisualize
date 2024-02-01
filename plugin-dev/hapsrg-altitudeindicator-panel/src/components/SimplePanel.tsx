import React from 'react';
import { FieldType, PanelProps } from '@grafana/data';
import { SimpleOptions } from 'types';
import { css, cx } from '@emotion/css';
import { useStyles2, useTheme2 } from '@grafana/ui';
import { AttitudeIndicator } from '../libs/react-flight-indicators';


interface Props extends PanelProps<SimpleOptions> {}

const getStyles = () => {
  return {
    wrapper: css`
      font-family: Open Sans;
      position: relative;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;      
    `,
    svg: css`
      position: absolute;
      top: 0;
      left: 0;
    `,
    textBox: css`
      position: absolute;
      bottom: 0;
      left: 0;
      padding: 10px;
    `,
  };
};

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
  const theme = useTheme2();
  const styles = useStyles2(getStyles);
  //   const headingValue = 180;
  // データフレームからheadingValueを取得する例
  const frame = data.series[0];
  let rollValue = 0; // デフォルト値
  let pitchValue = 0; // デフォルト値
  if (frame.length > 0 && frame.fields.length > 0) {
    const headingField = frame.fields.find(field => field.type === FieldType.number); 
    if (headingField && headingField.values.length > 0) {
      headingValue = headingField.values.get(0); // 最初の値を取得
    }
  }
  return (
    <div className={styles.wrapper}>
      <AltitudeIndicator
        pitch={headingValue}
        roll={rollValue}
        style={{ width: '100%', height: 'auto', maxWidth: '100%', maxHeight: '100%' }}
      />
    </div>
  );
};
