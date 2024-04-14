/*
Project file for controlling the gait-algorithm of the Y-robot for Bio inspired robotics project

Using board [Arduino UNO R3]
With shield [TA0039 Sensor Expansion Shield V5.0] (https://makerhero.com/img/files/download/TA0039-Datasheet.pdf)
To control servo [Fitec FS90 9G Mini Servo] (https://www.addicore.com/products/feetech-fitec-fs90-9g-mini-servo-with-accessories)

Servo has cables:
Brown    = Ground
Red      = Power
Yellow   = Signal

Servo can have pins >= 2, since 0 and 1 are interfered with by Serial connection.

This file takes a gait description vector and creates a series of motor inputs for the arduino
*/

#include <matplot/matplot.h>
#include <iostream>
#include <vector>
#include <chrono>
#include <thread>

#define GAIT_T 3.7    //Duration of the gait's repeating pattern (seconds)
#define GAIT_AMP 0.83  //Amplitude of the gait (0-1)


struct motorCMD{
  int motorID;
  float amount;
  float start;
  float duration;
};

std::vector<motorCMD> Gait_1 = {motorCMD{1,0.9,0.0,0.3}, 
                                motorCMD{2,0.9,0.0,0.3},
                                motorCMD{3,0.6,0.3,0.2},
                                motorCMD{1,0.5,0.3,0.2}, 
                                motorCMD{2,0.5,0.3,0.2},
                                motorCMD{1,0.0,0.5,0.3},
                                motorCMD{2,0.0,0.5,0.3},
                                motorCMD{3,0.0,0.8,0.2}};


void testWorkFunction(int max = 40){
  using namespace std::chrono;

  int rand_work = 2 + (std::rand() % ((max + 5) - 2 + 1));

  milliseconds work_time(rand_work);
  std::cout << "Work time: " << work_time.count() << std::endl;
  
  std::this_thread::sleep_for(work_time);
  return;
}

std::vector<float> gaitControl(std::vector<motorCMD> gait, std::chrono::microseconds deltaT = std::chrono::microseconds(0)){
  static float M1_pos = 0.0, M2_pos = 0.0, M3_pos = 0.0;
  static float T_in_gait = 0.0, T_elapsed = 0.0;

  //Incrementing the timing of the current gait
  float deltaT_sec = deltaT.count() * 0.000001;
  T_in_gait += deltaT_sec;
  T_elapsed += deltaT_sec;
  //std::cout << T_in_gait << std::endl;
  
  if(T_in_gait >= GAIT_T){ 
    //Wrap around if the timing is exceeding the gait period
    T_in_gait -= GAIT_T;
  }

  for(const auto& cmd : gait){
    float cmd_start_time = cmd.start * GAIT_T, cmd_end_time = (cmd.start + cmd.duration) * GAIT_T;
    if(T_in_gait >= cmd_start_time && T_in_gait < cmd_end_time){
      float elapsed_time_in_cmd = (T_in_gait - cmd_start_time) / (cmd_end_time - cmd_start_time);

      switch (cmd.motorID){
        case 1:
          M1_pos = M1_pos + ((cmd.amount * GAIT_AMP) - M1_pos) * elapsed_time_in_cmd;
          break;
        case 2:
          M2_pos = M2_pos + ((cmd.amount * GAIT_AMP) - M2_pos) * elapsed_time_in_cmd;
          break;
        case 3:
          M3_pos = M3_pos + ((cmd.amount * GAIT_AMP) - M3_pos) * elapsed_time_in_cmd;
          break;
        default:
          std::cerr << "Invalid motor ID" << std::endl;
      }

      std::cout << "["<< T_elapsed << "]: Motor " << cmd.motorID << " going to pos: " << cmd.amount * GAIT_AMP << " at time [" << T_in_gait << "]" << std::endl;
    }
  }

  std::cout << "["<< T_elapsed << "]: Motor positions: [" << M1_pos << ", " << M2_pos << ", " << M3_pos << "]" << std::endl;

  return {T_elapsed, M1_pos, M2_pos, M3_pos};
}


int main(int argc, char* argv[]){
  using namespace std::chrono;

  //The interval of which the motor commands are calculated (motor ticks):
  float tick_frq = 25; //Hz
  float time_ms = 1000/tick_frq;
  milliseconds motor_tick((int)time_ms);
  std::cout << "A motor tick is: " << (int)time_ms << " ms" << std::endl;

  std::vector<std::vector<float>> motor_positions; 
  bool run = true;

  while(run){
    //Motor_tick start time
    auto tick_start = steady_clock::now();
    static auto last_call = tick_start;

    //INSERT CODE TO CALCULATE MOTOR COMMANDS BELOW:
    //testWorkFunction((int)time_ms);
    std::vector<float> new_motor_positions;
    if(tick_start == last_call){
      last_call = steady_clock::now();
      motor_positions.push_back(gaitControl(Gait_1));
    }
    else{
      auto now = steady_clock::now();
      microseconds deltaT = duration_cast<microseconds>(now - last_call);
      last_call = now;
      motor_positions.push_back(gaitControl(Gait_1, deltaT));
    }

    auto work_complete = steady_clock::now();
    auto work_duration = duration_cast<milliseconds>(work_complete - tick_start);

    auto time_to_sleep = motor_tick - work_duration;
    if(time_to_sleep > milliseconds(0)){
      //Sleep remaining time of tick
      std::this_thread::sleep_for(time_to_sleep);
    }
    else{
      auto time_e = duration_cast<milliseconds>(time_to_sleep);
      std::cout << "Work is taking too long, timing issue of " << time_e.count() << " milliseconds" << std::endl;
    }
    auto tick_end = steady_clock::now();
    auto tick_duration = duration_cast<milliseconds>(tick_end - tick_start);
    //std::cout << "Tick timing: " << tick_duration.count() << std::endl;

    if(!motor_positions.empty()){
      if(motor_positions.back()[0] >= 25.0){
        run = false;
      }
      else{
        std::cout << "Time has not exceeded 25 seconds: " << motor_positions.back()[0] << std::endl;
      }
    }
    else{
      std::cout << "motor_positions is empty!" << std::endl;
    }
  }

  //Plotting the gait after 25 seconds:
  std::vector<double> time, M1, M2, M3;
  for(const auto& command_list : motor_positions){
    if(command_list.size() < 4){
      std::cerr << "Error: Each entry should have exactly 4 elements" << std::endl;
      return 1;
    }
    time.push_back(command_list[0]);
    M1.push_back(command_list[1]);
    M2.push_back(command_list[2]);
    M3.push_back(command_list[3]);
  }
  //Plotting:
  using namespace matplot;
  plot(time, M1, "r-")->line_width(2);
  hold(on);
  plot(time, M2, "g-")->line_width(2);
  plot(time, M3, "b-")->line_width(2);
  hold(off);
  xlabel("Time");
  ylabel("Motor pos");
  legend({"Motor1", "Motor2", "Motor3"});
  std::string title_str = "Gait Period: " + std::to_string(GAIT_T) + "s, Gait Amplitude Gain: " + std::to_string(GAIT_AMP);
  title(title_str);
  show();

  return 0;
}