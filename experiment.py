# -*- coding: utf-8 -*-

__author__ = "Austin Hurst"

import klibs
from klibs import P
from klibs.KLUtilities import deg_to_px, px_to_deg, flush, pump
from klibs.KLTime import CountDown
from klibs.KLUserInterface import any_key, ui_request, key_pressed
from klibs.KLGraphics import KLDraw as kld
from klibs.KLGraphics import fill, flip, blit
from klibs.KLCommunication import message
from klibs.KLAudio import Tone
from klibs.KLResponseCollectors import KeyPressResponse

import random
from copy import copy

# Define colours for the experiment

WHITE = [255, 255, 255, 255]
BLACK = [0, 0, 0, 255]
GREY = [128, 128, 128, 255]
RED = [255, 0, 0, 255]


class ANTI_VEA(klibs.Experiment):

    def setup(self):
        
        # Stimulus sizes
        
        fixation_size = deg_to_px(0.32)
        fixation_thickness = deg_to_px(0.08)
        cue_size = deg_to_px(0.64)
        cue_thickness = deg_to_px(0.08)
        arrow_tail_len = deg_to_px(0.48)
        arrow_tail_width = deg_to_px(0.15)
        arrow_head_len = deg_to_px(0.25)
        arrow_head_width = deg_to_px(0.45, even=True)
        arrow_dimensions = [arrow_tail_len, arrow_tail_width, arrow_head_len, arrow_head_width]
        
        # Stimuli
        
        self.warning_tone = Tone(50.1, 'sine', frequency=2000, volume=0.5)
        self.fixation = kld.FixationCross(fixation_size, fixation_thickness, fill=BLACK)
        self.cue = kld.Asterisk(cue_size, thickness=cue_thickness, fill=BLACK, spokes=8)
        self.arrow_r = kld.Arrow(*arrow_dimensions, fill=BLACK)
        self.arrow_l = kld.Arrow(*arrow_dimensions, fill=BLACK, rotation=180)
        self.arrow_r.render()
        self.arrow_l.render()
        
        # Layout
        
        self.height_offset = deg_to_px(1.3)
        self.height_jitter = deg_to_px(0.04)
        self.flanker_offset = arrow_tail_len + arrow_head_len + deg_to_px(0.16)
        self.ev_offsets = {'above': -(self.height_jitter*4), 'below': self.height_jitter*4}
        
        self.above_loc = (P.screen_c[0], P.screen_c[1]-self.height_offset)
        self.below_loc = (P.screen_c[0], P.screen_c[1]+self.height_offset)
        
        self.cue_locations = {'above': self.above_loc, 'below': self.below_loc}
        
        # Add text styles for PVT and block messages
        
        self.txtm.add_style("PVT", '1.5deg', color=RED)
        self.txtm.add_style("block_msg", '0.6deg', color=BLACK)

        # If it's the first session, insert practice blocks with feedback

        if P.run_practice_blocks and P.session_number == 1:
            ANTI_only = ['ANTI-valid', 'ANTI-invalid', 'ANTI-none']
            ANTI_EV = copy(ANTI_only) * 2 + ['EV-above', 'EV-below'] * 3 # 1/2 ANTI, 1/2 EV
            ANTI_EV_AV = copy(ANTI_EV) + ['AV'] * 6 # 1/3 ANTI, 1/3 EV, 1/3 AV
            self.insert_practice_block(1, trial_counts=16, factor_mask={'trial_type': ANTI_only})
            self.insert_practice_block(2, trial_counts=32, factor_mask={'trial_type': ANTI_EV})
            self.insert_practice_block(3, trial_counts=48, factor_mask={'trial_type': ANTI_EV_AV})
        

    def block(self):

        halfway_block = (P.blocks_per_experiment / 2) + 1
        if P.run_practice_blocks and P.session_number == 1:
            halfway_block += 3
        
        if P.run_practice_blocks and P.session_number == 1 and P.block_number <= 3:
            txt = "This is a practice block ({0} of 3)\n\n".format(P.block_number)
            if P.block_number == 1:
                txt += (
                    "During this task, arrows will appear either above or below the '+' symbol.\n"
                    "Your job will be to indicate the direction of the middle arrow as quickly\n"
                    "and accurately as possible using the keyboard.\n\n"
                    "( c = left,  m = right )"
                )
            elif P.block_number == 2:
                txt += (
                    "On some trials, the central arrow will be displaced upwards or downwards "
                    "by a large amount.\n"
                    "When this occurs, please press the space bar instead of the 'c' or 'm' keys."
                )
                self.trial_type = 'EV'
                self.ev_offset = 'below'
                demo_arrows = self.generate_arrows()
            else:
                txt += (
                    "On some trials, a large red countdown timer will appear instead of the arrows."
                    "\nWhen this occurs, please press the space bar as quickly as you can."
                )

            instructions = message(txt, align='center', blit_txt=False)
            continue_msg = message('Press any key to begin.', align='center', blit_txt=False)
            instruction_time = CountDown(3)
            while True:
                keydown = key_pressed()
                fill()
                blit(instructions, 8, (P.screen_c[0], int(P.screen_y*0.1)))
                if P.block_number == 2:
                    blit(self.fixation, 5, P.screen_c)
                    for shape, loc in demo_arrows:
                        blit(shape, 5, loc)
                elif P.block_number == 3:
                    elapsed = min([int(instruction_time.elapsed()*1000), 367])
                    demo_counter = message(str(elapsed).zfill(4), "PVT", blit_txt=False)
                    blit(demo_counter, 5, P.screen_c)
                if P.development_mode or instruction_time.counting() == False:
                    blit(continue_msg, 2, (P.screen_c[0], int(P.screen_y*0.9)))
                    if keydown == True:
                        break
                flip()

        elif P.run_practice_blocks and P.session_number == 1 and P.block_number == 4:
            self.block_msg("Practice complete! Press any key to begin the task.")

        elif P.block_number == 1:
            self.block_msg("Press any key to begin the task.")
            
        elif P.block_number == halfway_block:
            self.block_msg("Phew, you're halfway done! Press any key to continue.")
            

    def setup_response_collector(self):
        
        if 'ANTI' in self.trial_type:
            self.trial_type, self.cue_type = self.trial_type.split('-')
            self.ev_offset = None
        elif 'EV' in self.trial_type:
            self.trial_type, self.ev_offset = self.trial_type.split('-')
            self.cue_type = random.choice(['valid', 'invalid', 'none'])
        elif self.trial_type == 'AV':
            self.ev_offset = None
            self.cue_type = 'none'
            
        if self.cue_type == 'none':
            self.cue_location = None
        elif self.cue_type == 'valid':
            self.cue_location = self.target_location
        else:
            self.cue_location = 'above' if self.target_location == 'above' else 'below'
            
        # Set up Response Collector to get keypress responses
        
        if self.trial_type == 'AV':
            rc_callback = self.PVT_callback
            timeout = 1000
        else:
            rc_callback = self.ANT_callback
            timeout = 2000
        
        self.rc.uses(KeyPressResponse)
        self.rc.terminate_after = [timeout, klibs.TK_MS]
        self.rc.display_callback = rc_callback
        self.rc.keypress_listener.interrupts = True
        self.rc.keypress_listener.key_map = {'c': 'left', 'm': 'right', ' ': 'detection'}
        

    def trial_prep(self):
        
        self.target_direction = random.choice(['left', 'right'])
        self.targets_removed = False
        self.arrows = self.generate_arrows()

        # Ensure that tones are not played on PVT trials

        if self.trial_type == 'AV':
            self.tone_trial = False

        # Add timecourse of events to EventManager
        
        self.tone_onset = random.randrange(400, 1650, 50)

        events = []
        events.append(['tone_on',    self.tone_onset])
        events.append(['tone_off',   events[-1][1] + 50])
        events.append(['cue_on',     events[-1][1] + 350])
        events.append(['cue_off',    events[-1][1] + 50])
        events.append(['target_on',  events[-1][1] + 50])
        events.append(['target_off', events[-1][1] + 200])
        events.append(['trial_end',  4100])
        for e in events:
            self.evm.register_ticket(e)


    def trial(self):
        
        tone_played = False

        while self.evm.before('target_on', pump_events=True):
            fill()
            blit(self.fixation, 5, P.screen_c)
            if self.evm.between('cue_on', 'cue_off') and self.cue_location != None:
                loc = self.cue_locations[self.cue_location]
                blit(self.cue, 5, loc)
            if self.tone_trial and self.evm.after('tone_on'):
                if not tone_played:
                    self.warning_tone.play()
                    tone_played = True
            flip()
        
        if self.trial_type in ['ANTI', 'EV']:
            fill()
            blit(self.fixation, 5, P.screen_c)
            for shape, loc in self.arrows:
                blit(shape, 5, loc)
            flip()
        self.rc.collect()
        
        # Get response data and preprocess it before logging to database
        response, rt = self.rc.keypress_listener.response()
        if rt == klibs.TIMEOUT:
            response = 'NA'
        
        # if ANT trial, determine absolute diff. between y of central arrow and nearest flanker
        if self.trial_type != 'AV': 
            ylocs = [arrow[1][1] for arrow in self.arrows]
            l_diff = abs(ylocs[2] - ylocs[1])
            r_diff = abs(ylocs[2] - ylocs[3])
            abs_diff = px_to_deg(min([l_diff, r_diff]))
        else:
            abs_diff = 'NA'

        if self.trial_type == 'ANTI':
            self.ev_offset = 'NA'
            accuracy = int(response == self.target_direction)
        elif self.trial_type == 'EV':
            accuracy = int(response == 'detection')
        elif self.trial_type == 'AV':
            self.ev_offset = 'NA'
            self.target_direction = 'NA'
            self.target_location = 'NA'
            self.congruent = 'NA'
            accuracy = int(response == 'detection')
        
        if response == 'NA':
            accuracy = 'NA'

        if P.practicing and accuracy is not 1:
            # If on a practice block, show feedback if an incorrect response is made.
            if accuracy is 0:
                feedback = "Incorrect response!\n"
                if 'ANTI' in self.trial_type:
                    feedback += "Please press 'c' for left arrows and 'm' for right arrows."
                elif 'EV' in self.trial_type:
                    feedback += "Please press the space bar for displaced arrows."
                else:
                    feedback += "Please press the space bar for countdown timers."
            else:
                feedback = ("No valid response made!\n"
                    "Please press 'c' for left arrows, 'm' for right arrows, "
                    "and space for displaced arrows or countdowns.")

            feedback_msg = message(feedback, 'block_msg', blit_txt=False, align='center')
            fill()
            blit(feedback_msg, 5, P.screen_c)
            flip()
            flush()
            any_key()
            # After feedback acknowledged, return to fixation screen
            fill()
            blit(self.fixation, 5, P.screen_c)
            flip()

        else:
            while self.evm.before('trial_end', pump_events=True):
                fill()
                blit(self.fixation, 5, P.screen_c)
                flip()

        return {
            "session_num": P.session_number,
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "trial_type": self.trial_type,
            "warning_tone": self.tone_trial,
            "cue_type": self.cue_type,
            "target_location": self.target_location,
            "target_direction": self.target_direction,
            "congruent": self.congruent,
            "displacement": self.ev_offset,
            "abs_displacement": abs_diff, # diff. in dva between middle arrow and nearest flanker
            "response": response,
            "accuracy": accuracy,
            "rt": rt
        }


    def trial_clean_up(self):
        pass
        
        
    def clean_up(self):
        pass

    
    def generate_arrows(self):
        
        if self.target_location == 'above':
            base_height = P.screen_c[1] - self.height_offset
        else:
            base_height = P.screen_c[1] + self.height_offset
        
        min_y = base_height - self.height_jitter
        max_y = base_height + self.height_jitter
        
        if self.target_direction == 'left':
            target_arrow = self.arrow_l
            flanker_arrow = self.arrow_l if self.congruent else self.arrow_r
        else:
            target_arrow = self.arrow_r
            flanker_arrow = self.arrow_r if self.congruent else self.arrow_l  
        
        arrows = []
        for offset in [-2, -1, 0, 1, 2]:
            x = P.screen_c[0] + (offset * self.flanker_offset)
            if offset == 0 and self.trial_type == 'EV':
                y = base_height + self.ev_offsets[self.ev_offset]
            else:
                y = random.randint(min_y, max_y)
            arrow = ( target_arrow if offset == 0 else flanker_arrow, (x,y) )
            arrows.append(arrow)
            
        return arrows
        
        
    def ANT_callback(self):
        
        if self.evm.after('target_off') and not self.targets_removed:
            fill()
            blit(self.fixation, 5, P.screen_c)
            flip()
            self.targets_removed == True
            
    
    def PVT_callback(self):
        
        # Get time elapsed since callback start
        try:
            elapsed = int(self.evm.trial_time_ms - self.rc.rc_start_time)
        except TypeError: # if on first flip, before rc_start_time set
            elapsed = 0
        
        # Pad time elapsed with zeroes and render to text
        elapsed_msg = message(str(elapsed).zfill(4), "PVT", blit_txt=False)
        
        # Draw time elapsed to screen
        fill()
        blit(elapsed_msg, 5, P.screen_c)
        flip()
    
    
    def block_msg(self, text):
        
        msg = message(text, 'block_msg', blit_txt=False)
        fill()
        blit(msg, 5, P.screen_c)
        flip()
        flush()
        any_key()
        