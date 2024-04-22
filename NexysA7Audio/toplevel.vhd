library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
--The IEEE.std_logic_unsigned contains definitions that allow 
--std_logic_vector types to be used with the + operator to instantiate a 
--counter.
use IEEE.std_logic_unsigned.all;

entity toplevel is
Port (
        CLK 		 : in  STD_LOGIC;
        recordEnable : in STD_LOGIC;
        audioBits    : out STD_LOGIC_VECTOR(15 downto 0);
        micClk       : out STD_LOGIC;
        micLRSel     : out STD_LOGIC;
        micData      : in STD_LOGIC;
        ampPWM       : out STD_LOGIC;
        ampSD        : out STD_LOGIC	
    );
end toplevel;

architecture Behavioral of toplevel is
constant dataWidth : integer := 8000000; -- 8000000 bits = 1 megabyte

signal clk_cntr_reg : std_logic_vector (4 downto 0) := (others=>'0'); 

signal pwm_val_reg : std_logic := '0';
signal pwm_val_reg2 : std_logic_vector(dataWidth - 1 downto 0);
signal i,j : integer := 0;

begin

----------------------------------------------------------
------              MIC Control                    -------
----------------------------------------------------------
--PDM data from the microphone is registered on the rising 
--edge of every micClk, converting it to PWM. The PWM data
--is then connected to the mono audio out circuit, causing 
--the sound captured by the microphone to be played over 
--the audio out port.

process(CLK)
begin
  if (rising_edge(CLK)) then
    clk_cntr_reg <= clk_cntr_reg + 1;
  end if;
end process;

--micClk = 100MHz / 32 = 3.125 MHz
micClk <= clk_cntr_reg(4);

process(CLK)
begin
  if (rising_edge(CLK) and recordEnable = '1') then
    if (clk_cntr_reg = "01111" and i /= dataWidth) then
      pwm_val_reg2(i) <= micData;
      pwm_val_reg <= micData;
      i <= i+1;
    end if;
  end if;
end process;

process(CLK)
begin
  if (rising_edge(CLK)) then
    if (j /= dataWidth) then
        ampPWM <= pwm_val_reg2(j);
        j <= j + 1;
    else
        j <= 0;
    end if;
  end if;
end process;

micLRSel <= '0';
audioBits <= pwm_val_reg2(15 downto 0);
ampSD <= '1';

end Behavioral;
