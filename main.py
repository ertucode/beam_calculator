from beam_calculator import BeamCalculator

if __name__ == "__main__":
    beam_length = 10
    b = BeamCalculator(beam_length)
    b.load_from_json("samples/simply_supported_force_dist.json")
    b.mainloop()