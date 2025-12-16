// Copyright 2025 ETH Zurich and University of Bologna.
// Solderpad Hardware License, Version 0.51, see LICENSE for details.
// SPDX-License-Identifier: SHL-0.51


// A dummy package for the header file, since verilator
// requires a top-level or package for linting
package test_package;
  `include "addrmap.svh"

  function automatic int dummy_function();
    return 42;
  endfunction;

endpackage;
