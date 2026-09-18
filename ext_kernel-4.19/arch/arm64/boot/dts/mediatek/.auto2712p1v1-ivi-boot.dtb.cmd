cmd_arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dtb := mkdir -p arch/arm64/boot/dts/mediatek/ ; aarch64-openwrt-linux-musl-gcc -E -Wp,-MD,arch/arm64/boot/dts/mediatek/.auto2712p1v1-ivi-boot.dtb.d.pre.tmp -nostdinc -I./scripts/dtc/include-prefixes -I./arch/arm64/boot/dts -I./arch/arm64/boot/dts/include -I./include/ -Iarch/arm64/boot/dts -undef -D__DTS__ -x assembler-with-cpp -o arch/arm64/boot/dts/mediatek/.auto2712p1v1-ivi-boot.dtb.dts.tmp arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dts ; ./scripts/dtc/dtc -O dtb -o arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dtb -b 0 -iarch/arm64/boot/dts/mediatek/ -i./scripts/dtc/include-prefixes -Wno-unit_address_vs_reg -Wno-unit_address_format -Wno-avoid_unnecessary_addr_size -Wno-alias_paths -Wno-graph_child_address -Wno-graph_port -Wno-simple_bus_reg -Wno-unique_unit_address -Wno-pci_device_reg  -d arch/arm64/boot/dts/mediatek/.auto2712p1v1-ivi-boot.dtb.d.dtc.tmp arch/arm64/boot/dts/mediatek/.auto2712p1v1-ivi-boot.dtb.dts.tmp ; cat arch/arm64/boot/dts/mediatek/.auto2712p1v1-ivi-boot.dtb.d.pre.tmp arch/arm64/boot/dts/mediatek/.auto2712p1v1-ivi-boot.dtb.d.dtc.tmp > arch/arm64/boot/dts/mediatek/.auto2712p1v1-ivi-boot.dtb.d

source_arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dtb := arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dts

deps_arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dtb := \
  arch/arm64/boot/dts/mediatek/mt2712e.dtsi \
  scripts/dtc/include-prefixes/dt-bindings/thermal/thermal.h \
  arch/arm64/boot/dts/mediatek/mt2712.dtsi \
  scripts/dtc/include-prefixes/dt-bindings/clock/mt2712-clk.h \
  scripts/dtc/include-prefixes/dt-bindings/gpio/gpio.h \
  scripts/dtc/include-prefixes/dt-bindings/interrupt-controller/irq.h \
  scripts/dtc/include-prefixes/dt-bindings/interrupt-controller/arm-gic.h \
  scripts/dtc/include-prefixes/dt-bindings/memory/mt2712-larb-port.h \
  scripts/dtc/include-prefixes/dt-bindings/phy/phy.h \
  scripts/dtc/include-prefixes/dt-bindings/power/mt2712-power.h \
  scripts/dtc/include-prefixes/dt-bindings/gce/mt2712-gce.h \
  scripts/dtc/include-prefixes/dt-bindings/reset/mt2712-resets.h \
  arch/arm64/boot/dts/mediatek/mt2712-pinfunc.h \
  scripts/dtc/include-prefixes/dt-bindings/pinctrl/mt65xx.h \
  arch/arm64/boot/dts/mediatek/auto2712p1v1-common.dtsi \
  arch/arm64/boot/dts/mediatek/mt2712-sched-energy.dtsi \

arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dtb: $(deps_arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dtb)

$(deps_arch/arm64/boot/dts/mediatek/auto2712p1v1-ivi-boot.dtb):
