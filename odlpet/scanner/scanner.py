import stir
import numpy as np

def get_scanner_names():
    all_names = stir.Scanner_list_all_names()
    names = [name_.split(',')[0].rstrip() for name_ in all_names.split('\n')[:-1]]
    return names

SCANNER_NAMES = get_scanner_names()

def _get_scanner_by_name(name):
    """
    Get a STIR scanner by name.
    """
    if name not in SCANNER_NAMES:
        raise ValueError("No default scanner of name {}".format(name))
    stir_scanner = stir.Scanner.get_scanner_from_name(name)
    return stir_scanner

def _scanner_from_stir(stir_scanner):
    """
    Convert a STIR scanner to a Scanner object.
    """
    scanner = Scanner()
    scanner.num_rings = stir_scanner.get_num_rings()
    scanner.num_dets_per_ring = stir_scanner.get_num_detectors_per_ring()
    scanner.voxel_size_xy = stir_scanner.get_default_bin_size()
    scanner.default_non_arc_cor_bins = stir_scanner.get_default_num_arccorrected_bins()
    scanner.intrinsic_tilt = stir_scanner.get_default_intrinsic_tilt()
    scanner.det_radius = stir_scanner.get_inner_ring_radius()
    scanner.ring_spacing = stir_scanner.get_ring_spacing()
    scanner.average_depth_of_inter = stir_scanner.get_average_depth_of_interaction()
    scanner.max_num_non_arc_cor_bins = stir_scanner.get_max_num_non_arccorrected_bins()
    scanner.axials_blocks_per_bucket = stir_scanner.get_num_axial_blocks_per_bucket()
    scanner.trans_blocks_per_bucket = stir_scanner.get_num_transaxial_blocks_per_bucket()
    scanner.axial_crystals_per_block = stir_scanner.get_num_axial_crystals_per_block()
    scanner.trans_crystals_per_block = stir_scanner.get_num_transaxial_crystals_per_block()
    scanner.axial_crystals_per_singles_unit = stir_scanner.get_num_axial_crystals_per_singles_unit()
    scanner.trans_crystals_per_singles_unit = stir_scanner.get_num_transaxial_crystals_per_singles_unit()
    scanner.num_detector_layers = stir_scanner.get_num_detector_layers()
    return scanner



def get_scanner_by_name(name):
    """
    Return a Scanner object from a named Scanner.
    """
    return _scanner_from_stir(_get_scanner_by_name(name))


def stir_get_STIR_geometry(_num_rings, _num_dets_per_ring,
                           _det_radius, _ring_spacing,
                           _average_depth_of_inter,
                           _voxel_size_xy,
                           _axial_crystals_per_block = 1, _trans_crystals_per_block= 1,
                           _axials_blocks_per_bucket = 1, _trans_blocks_per_bucket = 1,
                           _axial_crystals_per_singles_unit = 1, _trans_crystals_per_singles_unit = 1,
                           _num_detector_layers = 1, _intrinsic_tilt = 0,
                           max_num_non_arc_cor_bins=None,
                           _default_non_arc_cor_bins=None):

    if max_num_non_arc_cor_bins is None:
        # Roughly speaking number of detectors on the diameter
        # bin_size = (_det_radius*2) / (_num_dets_per_ring/2)
        max_num_non_arc_cor_bins = int(_num_dets_per_ring/2)

    if _default_non_arc_cor_bins is None:
        _default_non_arc_cor_bins = max_num_non_arc_cor_bins

    # TODO: use "Userdefined" instead? (should not change much)
    scanner = stir.Scanner.get_scanner_from_name('')

    scanner.set_num_rings(np.int32(_num_rings))
    scanner.set_num_detectors_per_ring(np.int32(_num_dets_per_ring))
    scanner.set_default_bin_size(np.float32(_voxel_size_xy))
    scanner.set_default_num_arccorrected_bins(np.int32(_default_non_arc_cor_bins))
    scanner.set_default_intrinsic_tilt(np.float32(_intrinsic_tilt))
    scanner.set_inner_ring_radius(np.float32(_det_radius))
    scanner.set_ring_spacing(np.float32(_ring_spacing))
    scanner.set_average_depth_of_interaction(np.float32(_average_depth_of_inter))
    scanner.set_max_num_non_arccorrected_bins(np.int32(max_num_non_arc_cor_bins))
    scanner.set_num_axial_blocks_per_bucket(np.int32(_axials_blocks_per_bucket))
    scanner.set_num_transaxial_blocks_per_bucket(np.int32(_trans_blocks_per_bucket))
    scanner.set_num_axial_crystals_per_block(np.int32(_axial_crystals_per_block))
    scanner.set_num_transaxial_crystals_per_block(np.int32(_trans_crystals_per_block))
    scanner.set_num_axial_crystals_per_singles_unit(np.int32(_axial_crystals_per_singles_unit))
    scanner.set_num_transaxial_crystals_per_singles_unit(np.int32(_trans_crystals_per_singles_unit))
    scanner.set_num_detector_layers(np.int32(_num_detector_layers))

    if _check_consistency(scanner):
        return scanner
    else:
        raise TypeError('Something is wrong in the scanner geometry.')


def _check_consistency(_scanner):
    return _scanner.check_consistency() == stir.Succeeded(stir.Succeeded.yes)

class Scanner():

    max_num_non_arc_cor_bins = None
    default_non_arc_cor_bins = None

    def get_stir_scanner(self):

        # Now create the STIR geometry
        stir_scanner = stir_get_STIR_geometry(
            self.num_rings,
            self.num_dets_per_ring,
            self.det_radius,
            self.ring_spacing,
            self.average_depth_of_inter,
            self.voxel_size_xy,
            self.axial_crystals_per_block,
            self.trans_crystals_per_block,
            self.axials_blocks_per_bucket,
            self.trans_blocks_per_bucket,
            self.axial_crystals_per_singles_unit,
            self.trans_crystals_per_singles_unit,
            self.num_detector_layers,
            self.intrinsic_tilt,
            self.max_num_non_arc_cor_bins,
            self.default_non_arc_cor_bins)

        return stir_scanner


class mCT(Scanner):
    # Detector x size in mm - plus the ring difference
    det_nx_mm = 6.25
    # Detector y size in mm - plus the ring difference
    det_ny_mm = 6.25
    # Total number of rings
    num_rings = 8
    # Total number of detectors per ring
    num_dets_per_ring = 112
    # Inner radius of the scanner (crystal surface)
    det_radius = 57.5 # in mm

    #
    # Additional things that STIR would like to know
    #
    average_depth_of_inter = 7.0 # in mm
    ring_spacing = det_ny_mm
    voxel_size_xy = 1.65 # in mm
    axial_crystals_per_block = 8
    trans_crystals_per_block = 7
    axials_blocks_per_bucket = 1
    trans_blocks_per_bucket = 16
    axial_crystals_per_singles_unit = 8
    trans_crystals_per_singles_unit = 0
    num_detector_layers = 1
    intrinsic_tilt = 0.0
