### Read-only registers
| # | Addr | Name | Bits | Type | Description |
| --- | --- | --- | --- | --- | --- |
| 0 | x00 | DEVICE_ID | [31:0]  | r | Identification register which always returns the value x5352424D which represents the ASCII string "SRBM" |
| 1  | x04 | N0_V | [31:0] | r | Neuron 0 voltage |
| 2  | x08 | N1_V | [31:0] | r | Neuron 1 voltage |
| 3  | x0C | N2_V | [31:0] | r | Neuron 2 voltage |
| 4  | x10 | N3_V | [31:0] | r | Neuron 3 voltage |
| 5  | x14 | N4_V | [31:0] | r | Neuron 4 voltage |
| 6  | x18 | N5_V | [31:0] | r | Neuron 5 voltage |
| 7  | x1c | N0_OUT_SUM | [31:0] | r | Neuron 0 output sum |
| 8  | x20 | N1_OUT_SUM | [31:0] | r | Neuron 1 output sum |
| 9  | x24 | N2_OUT_SUM | [31:0] | r | Neuron 2 output sum |
| 10  | x28 | N3_OUT_SUM | [31:0] | r | Neuron 3 output sum |
| 11  | x2c | N4_OUT_SUM | [31:0] | r | Neuron 4 output sum |
| 12  | x30 | N5_OUT_SUM | [31:0] | r | Neuron 5 output sum |

### Writable registers
| # | Addr | Name | Bits | Type | Description |
| --- | --- | --- | --- | --- | --- |
| 30  | x78 | AXIS_PKT_LEN | [9:0] | w | AXI-stream packet length, such that signal tlast is asserted every `AXIS_PKT_LEN` cycles. Should be equal to DMA transfer size to keep the DMA IP happy. |
| 31 | x7C | DECAY_EN | [0] | w | Enable neuron decay |
| 32 | 0x80 | WEIGHT_WR_EN | [0] | w | Weight memory write enable. Only used to force BRAMs, do not write to it! |
| 33  | x84 | N0_IN_MEAN | [15:0] | r/w | Neuron 0 input mean |
| 34 | x88 | N1_IN_MEAN | [15:0] | r/w | Neuron 1 input mean |
| 35  | x8c | N2_IN_MEAN | [15:0] | r/w | Neuron 2 input mean |
| 36  | x90 | N3_IN_MEAN | [15:0] | r/w | Neuron 3 input mean |
| 37  | x94 | N4_IN_MEAN | [15:0] | r/w | Neuron 4 input mean |
| 38  | x98 | N5_IN_MEAN | [15:0] | r/w | Neuron 5 input mean |
