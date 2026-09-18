cmd_arch/arm64/boot/dts/mediatek/mt8168-evb.dtb := mkdir -p arch/arm64/boot/dts/mediatek/ ; aarch64-openwrt-linux-musl-gcc -E -Wp,-MD,arch/arm64/boot/dts/mediatek/.mt8168-evb.dtb.d.pre.tmp -nostdinc -I./scripts/dtc/include-prefixes -I./arch/arm64/boot/dts -I./arch/arm64/boot/dts/include -I./include/ -Iarch/arm64/boot/dts -undef -D__DTS__ -x assembler-with-cpp -o arch/arm64/boot/dts/mediatek/.mt8168-evb.dtb.dts.tmp arch/arm64/boot/dts/mediatek/mt8168-evb.dts ; ./scripts/dtc/dtc -O dtb -o arch/arm64/boot/dts/mediatek/mt8168-evb.dtb -b 0 -iarch/arm64/boot/dts/mediatek/ -i./scripts/dtc/include-prefixes -Wno-unit_address_vs_reg -Wno-unit_address_format -Wno-avoid_unnecessary_addr_size -Wno-alias_paths -Wno-graph_child_address -Wno-graph_port -Wno-simple_bus_reg -Wno-unique_unit_address -Wno-pci_device_reg  -d arch/arm64/boot/dts/mediatek/.mt8168-evb.dtb.d.dtc.tmp arch/arm64/boot/dts/mediatek/.mt8168-evb.dtb.dts.tmp ; cat arch/arm64/boot/dts/mediatek/.mt8168-evb.dtb.d.pre.tmp arch/arm64/boot/dts/mediatek/.mt8168-evb.dtb.d.dtc.tmp > arch/arm64/boot/dts/mediatek/.mt8168-evb.dtb.d

source_arch/arm64/boot/dts/mediatek/mt8168-evb.dtb := arch/arm64/boot/dts/mediatek/mt8168-evb.dts

deps_arch/arm64/boot/dts/mediatek/mt8168-evb.dtb := \
  arch/arm64/boot/dts/mediatek/mt8168.dtsi \
  scripts/dtc/include-prefixes/dt-bindings/clock/mt8168-clk.h \
  scripts/dtc/include-prefixes/dt-bindings/iio/mt635x-auxadc.h \
  scripts/dtc/include-prefixes/dt-bindings/interrupt-controller/irq.h \
  scripts/dtc/include-prefixes/dt-bindings/interrupt-controller/arm-gic.h \
  scripts/dtc/include-prefixes/dt-bindings/phy/phy.h \
  scripts/dtc/include-prefixes/dt-bindings/pinctrl/mt8168-pinfunc.h \
  scripts/dtc/include-prefixes/dt-bindings/pinctrl/mt65xx.h \
  scripts/dtc/include-prefixes/dt-bindings/gpio/gpio.h \

arch/arm64/boot/dts/mediatek/mt8168-evb.dtb: $(deps_arch/arm64/boot/dts/mediatek/mt8168-evb.dtb)

$(deps_arch/arm64/boot/dts/mediatek/mt8168-evb.dtb):
